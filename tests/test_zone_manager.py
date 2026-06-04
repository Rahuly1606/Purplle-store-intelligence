import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.zones.zone_manager import ZoneManager

zone_manager = ZoneManager()

print(
    zone_manager.get_zone(
        100,
        100
    )
)

print(
    zone_manager.get_zone(
        500,
        200
    )
)

print(
    zone_manager.get_zone(
        900,
        200
    )
)