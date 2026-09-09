from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item

CATALOG_ITEMS = [
    {
        "slug": "lavender",
        "name": "Lavender",
        "description": "A gentle floral essence often chosen for calm routines and evening wind-downs.",
        "symptoms": ["stress", "sleep", "restless", "tension", "anxious", "calm"],
        "uses": ["Diffuse during quiet time", "Add to a bedtime aroma routine", "Pair with breathing exercises"],
        "safety_notes": ["Use as wellness support, not medical treatment", "Dilute before topical use"],
    },
    {
        "slug": "peppermint",
        "name": "Peppermint",
        "description": "A bright, cooling essence associated with clarity, focus, and refreshed breathing rituals.",
        "symptoms": ["headache", "focus", "nausea", "energy", "fatigue", "congestion"],
        "uses": ["Diffuse for an alert workspace", "Use diluted for a cooling aroma experience"],
        "safety_notes": ["Avoid contact with eyes", "Use extra caution around young children and pets"],
    },
    {
        "slug": "lemon",
        "name": "Lemon",
        "description": "A clean citrus essence used for an uplifting atmosphere and a sense of freshness.",
        "symptoms": ["energy", "clarity", "mood", "stale", "focus", "fresh"],
        "uses": ["Diffuse in the morning", "Use to brighten a study or kitchen space"],
        "safety_notes": ["May increase sun sensitivity if used topically", "Dilute before topical use"],
    },
    {
        "slug": "thieves",
        "name": "Thieves",
        "description": "A warm spice blend often selected for seasonal routines and a cozy, clean environment.",
        "symptoms": ["immune", "seasonal", "cold", "winter", "cozy", "stuffy"],
        "uses": ["Diffuse during seasonal changes", "Use in household aroma rituals"],
        "safety_notes": ["Spice oils can irritate skin; dilute well", "Use as general wellness support only"],
    },
    {
        "slug": "frankincense",
        "name": "Frankincense",
        "description": "A resinous, grounding essence commonly used for meditation and reflective practices.",
        "symptoms": ["grounding", "meditation", "stress", "overwhelmed", "focus", "balance"],
        "uses": ["Diffuse during meditation", "Use in a grounding evening ritual"],
        "safety_notes": ["Dilute before topical use", "Discontinue use if irritation occurs"],
    },
    {
        "slug": "copaiba",
        "name": "Copaiba",
        "description": "A soft, woody essence often chosen for comfort-focused routines after busy days.",
        "symptoms": ["discomfort", "tension", "sore", "aches", "recovery", "relax"],
        "uses": ["Use diluted in a comfort massage routine", "Diffuse for a mellow atmosphere"],
        "safety_notes": ["Not a substitute for medical care", "Dilute before topical use"],
    },
]


def seed_catalog(session: Session) -> None:
    existing_slugs = set(session.scalars(select(Item.slug)).all())
    for item_data in CATALOG_ITEMS:
        if item_data["slug"] not in existing_slugs:
            session.add(Item(**item_data))
    session.commit()
