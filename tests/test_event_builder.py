import sys
from pathlib import Path

# Add project root to path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.events.event_builder import EventBuilder


def main():

    event = EventBuilder.entry_event(
        visitor_id="VIS_001",
        store_id="STORE_BLR_001",
        camera_id="CAM_ENTRY_01"
    )

    print(event)


if __name__ == "__main__":
    main()