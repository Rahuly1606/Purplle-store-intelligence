from uuid import uuid4
from datetime import (
    datetime,
    timezone
)


class EventBuilder:

    @staticmethod
    def build_event(
        event_type,
        visitor_id,
        store_id,
        camera_id,
        zone_id=None,
        dwell_ms=0,
        is_staff=False,
        confidence=1.0,
        metadata=None
    ):

        if metadata is None:
            metadata = {}

        return {

            "event_id":
                str(uuid4()),

            "store_id":
                store_id,

            "camera_id":
                camera_id,

            "visitor_id":
                visitor_id,

            "event_type":
                event_type,

            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "zone_id":
                zone_id,

            "dwell_ms":
                dwell_ms,

            "is_staff":
                is_staff,

            "confidence":
                confidence,

            "metadata":
                metadata
        }