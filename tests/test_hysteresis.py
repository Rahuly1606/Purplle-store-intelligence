from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.zones.hysteresis_manager import HysteresisManager

manager = HysteresisManager(
    threshold=3
)

zones = [
    "ENTRY",
    "ENTRY",
    "SKINCARE",
    "ENTRY",
    "SKINCARE",
    "SKINCARE",
    "SKINCARE"
]

for zone in zones:

    print(
        manager.update(
            1,
            zone
        )
    )