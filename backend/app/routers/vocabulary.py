from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.spaced_repetition import SpacedRepetitionService
from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/vocabulary", tags=["vocabulary"])

@router.get("/review-words")
async def get_review_words(
    session_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get words due for review using spaced repetition algorithm."""
    try:
        service = SpacedRepetitionService()
        words = await service.get_words_for_review(
            user_id=str(current_user.id),
            session_size=session_size,
            db=db
        )
        return words
    except Exception as e:
        logger.error(f"Error getting review words: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get review words"
        )

@router.post("/review-response")
async def submit_review_response(
    vocabulary_id: str,
    quality: int,
    response_time_ms: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Submit a review response and get next review interval."""
    if not 0 <= quality <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quality must be between 0 and 5"
        )
    
    try:
        service = SpacedRepetitionService()
        result = await service.process_review_response(
            user_id=str(current_user.id),
            vocabulary_id=vocabulary_id,
            quality=quality,
            response_time_ms=response_time_ms,
            db=db
        )
        return result
    except Exception as e:
        logger.error(f"Error processing review response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process review response"
        )

@router.get("/statistics")
async def get_learning_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get comprehensive learning statistics for the current user."""
    try:
        service = SpacedRepetitionService()
        stats = await service.get_learning_statistics(
            user_id=str(current_user.id),
            db=db
        )
        return stats
    except Exception as e:
        logger.error(f"Error getting learning statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get learning statistics"
        )
