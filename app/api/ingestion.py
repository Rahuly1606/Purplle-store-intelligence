import json

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.event_batch import EventBatch

from app.database.database import get_db
from app.database.models import EventDB

router = APIRouter()

@router.post("/events/ingest")
def ingest_events(
    payload: EventBatch,
    db: Session = Depends(get_db)
):

    accepted = 0
    rejected = 0

    errors = []

    for event in payload.events:

        existing = db.get(
            EventDB,
            event.event_id
        )

        if existing:
            continue

        row = EventDB(
            event_id=event.event_id,
            store_id=event.store_id,
            camera_id=event.camera_id,
            visitor_id=event.visitor_id,
            event_type=event.event_type,
            timestamp=str(event.timestamp),
            zone_id=event.zone_id,
            dwell_ms=event.dwell_ms,
            is_staff=event.is_staff,
            confidence=event.confidence,
            metadata_json=json.dumps(
                event.metadata.model_dump()
            )
        )

        db.add(row)

        accepted += 1

    db.commit()

    return {
        "accepted": accepted,
        "rejected": rejected,
        "errors": errors
    }