from pydantic import BaseModel, ConfigDict, Field


class ChatRecommendationRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=3, ge=1, le=6)


class RecommendedEssence(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str
    symptoms: list[str]
    uses: list[str]
    safety_notes: list[str]
    score: int
    matched_symptoms: list[str]
    reasons: list[str]


class ChatRecommendationResponse(BaseModel):
    reply: str
    recommendations: list[RecommendedEssence]
    detected_symptoms: list[str]
