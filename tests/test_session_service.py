import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.services.session_service import SessionService


class Event:

    def __init__(
        self,
        visitor_id,
        event_type,
        zone_id=None,
        is_staff=False
    ):
        self.visitor_id = visitor_id
        self.event_type = event_type
        self.zone_id = zone_id
        self.is_staff = is_staff


events = [

    Event(
        "VIS_001",
        "ENTRY"
    ),

    Event(
        "VIS_001",
        "ZONE_ENTER",
        "ELECTRONICS"
    ),

    Event(
        "VIS_001",
        "BILLING_QUEUE_JOIN"
    )
]

sessions = SessionService.build_sessions(
    events
)

print(dict(sessions))