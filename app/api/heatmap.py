from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import EventDB

from app.services.heatmap_service import HeatmapService

router = APIRouter()


@router.get("/stores/{store_id}/heatmap")
def get_heatmap(
    store_id: str,
    db: Session = Depends(get_db)
):
    events = (
        db.query(EventDB)
        .filter(EventDB.store_id == store_id)
        .all()
    )

    return HeatmapService.calculate(events)