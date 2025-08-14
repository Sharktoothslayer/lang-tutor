from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user_vocabulary_progress import UserVocabularyProgress
from app.models.vocabulary import Vocabulary
from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)

class SpacedRepetitionService:
    """
    Implements the SuperMemo 2 (SM-2) spaced repetition algorithm
    for optimal vocabulary learning intervals.
    """
    
    def __init__(self):
        self.min_ease_factor = 1.3
        self.initial_ease_factor = 2.5
    
    async def get_words_for_review(
        self, 
        user_id: str, 
        session_size: int = 20,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """
        Get words that are due for review based on spaced repetition algorithm.
        """
        if not db:
            db = await anext(get_db())
        
        try:
            # Get words due for review
            query = select(UserVocabularyProgress).where(
                UserVocabularyProgress.user_id == user_id,
                UserVocabularyProgress.next_review <= datetime.utcnow()
            ).order_by(UserVocabularyProgress.next_review.asc())
            
            result = await db.execute(query)
            due_words = result.scalars().all()
            
            # Get new words if we don't have enough due words
            new_words_needed = max(0, session_size - len(due_words))
            new_words = []
            
            if new_words_needed > 0:
                new_words = await self._get_new_words(user_id, new_words_needed, db)
            
            # Combine and format results
            review_words = []
            for progress in due_words[:session_size]:
                word_data = await self._get_word_data(progress.vocabulary_id, db)
                if word_data:
                    review_words.append({
                        'progress_id': str(progress.id),
                        'word_id': str(progress.vocabulary_id),
                        'word': word_data['word'],
                        'translation': word_data['translation'],
                        'part_of_speech': word_data['part_of_speech'],
                        'example_sentence': word_data['example_sentence'],
                        'pronunciation': word_data['pronunciation'],
                        'ease_factor': float(progress.ease_factor),
                        'interval': progress.interval,
                        'repetitions': progress.repetitions,
                        'mastery_level': progress.mastery_level
                    })
            
            return review_words + new_words
            
        except Exception as e:
            logger.error(f"Error getting words for review: {e}")
            return []
    
    async def _get_new_words(
        self, 
        user_id: str, 
        count: int, 
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Get new words that haven't been learned yet."""
        try:
            # Find words not in user's progress
            subquery = select(UserVocabularyProgress.vocabulary_id).where(
                UserVocabularyProgress.user_id == user_id
            )
            
                   query = select(Vocabulary).where(
                       Vocabulary.language_code == 'it'  # Default to Italian, make configurable
                   ).where(
                ~Vocabulary.id.in_(subquery)
            ).order_by(Vocabulary.difficulty_level.asc(), Vocabulary.frequency_rank.asc())
            
            result = await db.execute(query)
            new_words = result.scalars().limit(count).all()
            
            return [{
                'progress_id': None,
                'word_id': str(word.id),
                'word': word.word,
                'translation': word.translation,
                'part_of_speech': word.part_of_speech,
                'example_sentence': word.example_sentence,
                'pronunciation': word.pronunciation,
                'ease_factor': self.initial_ease_factor,
                'interval': 0,
                'repetitions': 0,
                'mastery_level': 0
            } for word in new_words]
            
        except Exception as e:
            logger.error(f"Error getting new words: {e}")
            return []
    
    async def _get_word_data(
        self, 
        vocabulary_id: str, 
        db: AsyncSession
    ) -> Optional[Dict[str, Any]]:
        """Get vocabulary word data."""
        try:
            query = select(Vocabulary).where(Vocabulary.id == vocabulary_id)
            result = await db.execute(query)
            word = result.scalar_one_or_none()
            
            if word:
                return {
                    'word': word.word,
                    'translation': word.translation,
                    'part_of_speech': word.part_of_speech,
                    'example_sentence': word.example_sentence,
                    'pronunciation': word.pronunciation
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting word data: {e}")
            return None
    
    async def process_review_response(
        self,
        user_id: str,
        vocabulary_id: str,
        quality: int,  # 0-5 scale (0=complete blackout, 5=perfect response)
        response_time_ms: Optional[int] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """
        Process a review response and calculate next review interval using SM-2 algorithm.
        
        Args:
            quality: Response quality (0-5)
                0: Complete blackout
                1: Incorrect response; the correct one remembered
                2: Incorrect response; where the correct one seemed easy to recall
                3: Correct response recalled with serious difficulty
                4: Correct response after some hesitation
                5: Perfect response with no hesitation
        """
        if not db:
            db = await anext(get_db())
        
        try:
            # Get or create progress record
            progress = await self._get_or_create_progress(user_id, vocabulary_id, db)
            
            # Calculate new values using SM-2 algorithm
            new_values = self._calculate_sm2_values(
                progress.ease_factor,
                progress.interval,
                progress.repetitions,
                quality
            )
            
            # Update progress
            await self._update_progress(progress.id, new_values, response_time_ms, db)
            
            return {
                'new_ease_factor': new_values['ease_factor'],
                'new_interval': new_values['interval'],
                'next_review': new_values['next_review'],
                'mastery_level': self._calculate_mastery_level(new_values['repetitions'], quality)
            }
            
        except Exception as e:
            logger.error(f"Error processing review response: {e}")
            raise
    
    def _calculate_sm2_values(
        self,
        ease_factor: float,
        interval: int,
        repetitions: int,
        quality: int
    ) -> Dict[str, Any]:
        """
        Calculate new values using the SM-2 algorithm.
        """
        # Calculate new ease factor
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Ensure ease factor doesn't go below minimum
        if new_ease_factor < self.min_ease_factor:
            new_ease_factor = self.min_ease_factor
        
        # Calculate new interval
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(interval * new_ease_factor)
        
        # Calculate next review date
        next_review = datetime.utcnow() + timedelta(days=new_interval)
        
        # Increment repetitions
        new_repetitions = repetitions + 1
        
        return {
            'ease_factor': new_ease_factor,
            'interval': new_interval,
            'repetitions': new_repetitions,
            'next_review': next_review
        }
    
    def _calculate_mastery_level(self, repetitions: int, quality: int) -> int:
        """Calculate mastery level based on repetitions and quality."""
        if repetitions >= 10 and quality >= 4:
            return 5  # Mastered
        elif repetitions >= 5 and quality >= 3:
            return 4  # Advanced
        elif repetitions >= 3 and quality >= 2:
            return 3  # Intermediate
        elif repetitions >= 1 and quality >= 1:
            return 2  # Beginner
        else:
            return 1  # New
    
    async def _get_or_create_progress(
        self,
        user_id: str,
        vocabulary_id: str,
        db: AsyncSession
    ) -> UserVocabularyProgress:
        """Get existing progress or create new one."""
        query = select(UserVocabularyProgress).where(
            UserVocabularyProgress.user_id == user_id,
            UserVocabularyProgress.vocabulary_id == vocabulary_id
        )
        
        result = await db.execute(query)
        progress = result.scalar_one_or_none()
        
        if not progress:
            # Create new progress record
            progress = UserVocabularyProgress(
                user_id=user_id,
                vocabulary_id=vocabulary_id,
                ease_factor=self.initial_ease_factor,
                interval=0,
                repetitions=0,
                next_review=datetime.utcnow(),
                mastery_level=1
            )
            db.add(progress)
            await db.commit()
            await db.refresh(progress)
        
        return progress
    
    async def _update_progress(
        self,
        progress_id: str,
        new_values: Dict[str, Any],
        response_time_ms: Optional[int],
        db: AsyncSession
    ):
        """Update progress record with new values."""
        update_query = update(UserVocabularyProgress).where(
            UserVocabularyProgress.id == progress_id
        ).values(
            ease_factor=new_values['ease_factor'],
            interval=new_values['interval'],
            repetitions=new_values['repetitions'],
            next_review=new_values['next_review'],
            last_review=datetime.utcnow(),
            total_reviews=UserVocabularyProgress.total_reviews + 1,
            correct_reviews=UserVocabularyProgress.correct_reviews + (1 if new_values['repetitions'] > 0 else 0)
        )
        
        await db.execute(update_query)
        await db.commit()
    
    async def get_learning_statistics(self, user_id: str, db: AsyncSession = None) -> Dict[str, Any]:
        """Get comprehensive learning statistics for a user."""
        if not db:
            db = await anext(get_db())
        
        try:
            # Get total words learned
            total_query = select(UserVocabularyProgress).where(
                UserVocabularyProgress.user_id == user_id
            )
            result = await db.execute(total_query)
            total_words = result.scalars().all()
            
            # Calculate statistics
            total_reviews = sum(word.total_reviews for word in total_words)
            correct_reviews = sum(word.correct_reviews for word in total_words)
            accuracy_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
            
            # Words by mastery level
            mastery_distribution = {}
            for word in total_words:
                level = word.mastery_level
                mastery_distribution[level] = mastery_distribution.get(level, 0) + 1
            
            # Words due for review
            due_words = [word for word in total_words if word.next_review <= datetime.utcnow()]
            
            return {
                'total_words_learning': len(total_words),
                'total_reviews': total_reviews,
                'correct_reviews': correct_reviews,
                'accuracy_rate': round(accuracy_rate, 2),
                'words_due_review': len(due_words),
                'mastery_distribution': mastery_distribution,
                'average_ease_factor': sum(word.ease_factor for word in total_words) / len(total_words) if total_words else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            return {} 