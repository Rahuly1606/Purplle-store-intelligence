from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import EventDB

from app.services.metrics_service import MetricsService

router = APIRouter()


@router.get("/stores/{store_id}/metrics")
def get_metrics(
    store_id: str,
    db: Session = Depends(get_db)
):
    events = (
        db.query(EventDB)
        .filter(EventDB.store_id == store_id)
        .all()
    )

    return MetricsService.calculate(events)