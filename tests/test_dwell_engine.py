from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.analytics.dwell_engine import DwellEngine

engine = DwellEngine()

engine.zone_enter(
    "VIS_1",
    "SKINCARE",
    100
)

result = engine.zone_exit(
    "VIS_1",
    "SKINCARE",
    145
)

print(result)

print(
    engine.get_zone_average(
        "SKINCARE"
    )
)