from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.recommendation import ChatRecommendationRequest, ChatRecommendationResponse
from app.services import items as item_service
from app.services.recommendations import recommend_essences

router = APIRouter()


@router.post("", response_model=ChatRecommendationResponse)
def create_recommendation(
    payload: ChatRecommendationRequest,
    session: Session = Depends(get_session),
) -> ChatRecommendationResponse:
    catalog = item_service.list_items(session)
    return recommend_essences(payload.message, catalog, payload.limit)
