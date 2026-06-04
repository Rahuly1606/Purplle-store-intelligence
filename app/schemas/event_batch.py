from typing import List
from pydantic import BaseModel

from app.schemas.event import Event


class EventBatch(BaseModel):
    events: List[Event]