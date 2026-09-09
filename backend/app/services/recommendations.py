import re

from app.models.item import Item
from app.schemas.recommendation import ChatRecommendationResponse, RecommendedEssence

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
WELLNESS_DISCLAIMER = "These are informational wellness suggestions, not medical advice."


def recommend_essences(message: str, catalog: list[Item], limit: int) -> ChatRecommendationResponse:
    normalized = message.lower()
    tokens = set(TOKEN_PATTERN.findall(normalized))
    scored: list[RecommendedEssence] = []
    detected_symptoms: set[str] = set()

    for item in catalog:
        matched = sorted({symptom for symptom in item.symptoms if _matches(symptom, normalized, tokens)})
        if not matched:
            continue

        detected_symptoms.update(matched)
        score = (len(matched) * 3) + _supporting_keyword_score(item, tokens)
        scored.append(
            RecommendedEssence(
                id=item.id,
                slug=item.slug,
                name=item.name,
                description=item.description,
                symptoms=item.symptoms,
                uses=item.uses,
                safety_notes=item.safety_notes,
                score=score,
                matched_symptoms=matched,
                reasons=[f"Matched your mention of {symptom}." for symptom in matched],
            )
        )

    recommendations = sorted(scored, key=lambda item: (-item.score, item.name))[:limit]
    if not recommendations:
        return ChatRecommendationResponse(
            reply=(
                "I could not identify a clear symptom pattern yet. Share whether you want support "
                "for sleep, stress, focus, energy, seasonal comfort, or body tension. "
                f"{WELLNESS_DISCLAIMER}"
            ),
            recommendations=[],
            detected_symptoms=[],
        )

    names = ", ".join(item.name for item in recommendations)
    return ChatRecommendationResponse(
        reply=f"Based on your message, consider exploring {names}. {WELLNESS_DISCLAIMER}",
        recommendations=recommendations,
        detected_symptoms=sorted(detected_symptoms),
    )


def _matches(symptom: str, normalized: str, tokens: set[str]) -> bool:
    symptom_text = symptom.lower()
    if " " in symptom_text:
        return symptom_text in normalized
    return symptom_text in tokens or any(token.startswith(symptom_text) for token in tokens)


def _supporting_keyword_score(item: Item, tokens: set[str]) -> int:
    supporting_text = " ".join([item.description, *item.uses]).lower()
    return sum(1 for token in tokens if len(token) > 3 and token in supporting_text)
