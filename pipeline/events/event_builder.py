from uuid import uuid4
from datetime import datetime, timezone


class EventBuilder:

    @staticmethod
    def entry_event(
        visitor_id,
        store_id,
        camera_id
    ):

        return {
            "event_id": str(uuid4()),

            "store_id": store_id,

            "camera_id": camera_id,

            "visitor_id": visitor_id,

            "event_type": "ENTRY",

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "zone_id": None,

            "dwell_ms": 0,

            "is_staff": False,

            "confidence": 1.0,

            "metadata": {
                "queue_depth": None,
                "sku_zone": None,
                "session_seq": 1
            }
        }