from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
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
    
    def get_words_for_review(
        self, 
        user_id: str, 
        session_size: int = 20,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """
        Get words that are due for review based on spaced repetition algorithm.
        """
        if not db:
            db = next(get_db())
        
        try:
            # Get words due for review
            query = select(UserVocabularyProgress).where(
                UserVocabularyProgress.user_id == user_id,
                UserVocabularyProgress.next_review <= datetime.utcnow()
            ).order_by(UserVocabularyProgress.next_review.asc())
            
            result = db.execute(query)
            due_words = result.scalars().all()
            
            # Get new words if we don't have enough due words
            new_words_needed = max(0, session_size - len(due_words))
            new_words = []
            
            if new_words_needed > 0:
                new_words = self._get_new_words(user_id, new_words_needed, db)
            
            # Combine and format results
            review_words = []
            for progress in due_words[:session_size]:
                word_data = self._get_word_data(progress.vocabulary_id, db)
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
    
    def _get_new_words(
        self, 
        user_id: str, 
        count: int, 
        db: Session
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
            
            result = db.execute(query)
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
    
    def _get_word_data(
        self, 
        vocabulary_id: str, 
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """Get vocabulary word data."""
        try:
            query = select(Vocabulary).where(Vocabulary.id == vocabulary_id)
            result = db.execute(query)
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
    
    def process_review_response(
        self,
        user_id: str,
        vocabulary_id: str,
        quality: int,  # 0-5 scale (0=complete blackout, 5=perfect response)
        response_time_ms: Optional[int] = None,
        db: Session = None
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
            db = next(get_db())
        
        try:
            # Get or create progress record
            progress = self._get_or_create_progress(user_id, vocabulary_id, db)
            
            # Calculate new values using SM-2 algorithm
            new_values = self._calculate_sm2_values(
                progress.ease_factor,
                progress.interval,
                progress.repetitions,
                quality
            )
            
            # Update progress
            self._update_progress(progress.id, new_values, response_time_ms, db)
            
            return {
                'new_ease_factor': new_values['ease_factor'],
                'new_interval': new_values['interval'],
                'next_review': new_values['next_review'],
                'mastery_level': self._calculate_mastery_level(new_values['repetitions'], quality)
            }
            
        except Exception as e:
            logger.error(f"Error processing review response: {e}")
            return {
                'new_ease_factor': 2.5,
                'new_interval': 1,
                'next_review': datetime.utcnow() + timedelta(days=1),
                'mastery_level': 0
            }
    
    def _get_or_create_progress(
        self, 
        user_id: str, 
        vocabulary_id: str, 
        db: Session
    ) -> UserVocabularyProgress:
        """Get existing progress or create new one."""
        query = select(UserVocabularyProgress).where(
            UserVocabularyProgress.user_id == user_id,
            UserVocabularyProgress.vocabulary_id == vocabulary_id
        )
        result = db.execute(query)
        progress = result.scalar_one_or_none()
        
        if not progress:
            progress = UserVocabularyProgress(
                user_id=user_id,
                vocabulary_id=vocabulary_id
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)
        
        return progress
    
    def _update_progress(
        self, 
        progress_id: str, 
        new_values: Dict[str, Any], 
        response_time_ms: Optional[int],
        db: Session
    ):
        """Update progress record with new values."""
        try:
            stmt = update(UserVocabularyProgress).where(
                UserVocabularyProgress.id == progress_id
            ).values(
                ease_factor=new_values['ease_factor'],
                interval=new_values['interval'],
                repetitions=new_values['repetitions'],
                next_review=new_values['next_review'],
                last_reviewed=datetime.utcnow(),
                total_reviews=UserVocabularyProgress.total_reviews + 1,
                correct_reviews=UserVocabularyProgress.correct_reviews + (1 if new_values['quality'] >= 3 else 0)
            )
            
            db.execute(stmt)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
            db.rollback()
    
    def _calculate_sm2_values(
        self, 
        ease_factor: float, 
        interval: int, 
        repetitions: int, 
        quality: int
    ) -> Dict[str, Any]:
        """Calculate new SM-2 values based on response quality."""
        if quality < 3:
            # Incorrect response - reset to beginning
            new_repetitions = 0
            new_interval = 1
        else:
            # Correct response
            new_repetitions = repetitions + 1
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = int(interval * ease_factor)
        
        # Calculate new ease factor
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease_factor = max(self.min_ease_factor, new_ease_factor)
        
        # Calculate next review date
        next_review = datetime.utcnow() + timedelta(days=new_interval)
        
        return {
            'ease_factor': new_ease_factor,
            'interval': new_interval,
            'repetitions': new_repetitions,
            'next_review': next_review,
            'quality': quality
        }
    
    def _calculate_mastery_level(self, repetitions: int, quality: int) -> int:
        """Calculate mastery level based on repetitions and quality."""
        if repetitions >= 5 and quality >= 4:
            return 5  # Mastered
        elif repetitions >= 3 and quality >= 3:
            return 4  # Advanced
        elif repetitions >= 2 and quality >= 3:
            return 3  # Intermediate
        elif repetitions >= 1 and quality >= 2:
            return 2  # Beginner
        else:
            return 1  # New
    
    def get_learning_statistics(
        self, 
        user_id: str, 
        db: Session = None
    ) -> Dict[str, Any]:
        """Get comprehensive learning statistics for a user."""
        if not db:
            db = next(get_db())
        
        try:
            # Get total words in progress
            total_query = select(UserVocabularyProgress).where(
                UserVocabularyProgress.user_id == user_id
            )
            total_result = db.execute(total_query)
            total_words = len(total_result.scalars().all())
            
            # Get mastered words
            mastered_query = select(UserVocabularyProgress).where(
                UserVocabularyProgress.user_id == user_id,
                UserVocabularyProgress.is_mastered == True
            )
            mastered_result = db.execute(mastered_query)
            mastered_words = len(mastered_result.scalars().all())
            
            # Calculate accuracy rate
            accuracy_query = select(UserVocabularyProgress).where(
                UserVocabularyProgress.user_id == user_id
            )
            accuracy_result = db.execute(accuracy_query)
            all_progress = accuracy_result.scalars().all()
            
            total_reviews = sum(p.total_reviews for p in all_progress)
            correct_reviews = sum(p.correct_reviews for p in all_progress)
            
            accuracy_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
            
            return {
                'total_words_learning': total_words,
                'mastered_words': mastered_words,
                'accuracy_rate': round(accuracy_rate, 2),
                'total_reviews': total_reviews,
                'correct_reviews': correct_reviews
            }
            
        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            return {} 