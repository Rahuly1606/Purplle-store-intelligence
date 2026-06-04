import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.events.state_manager import (
    StateManager
)

manager = StateManager()

print(
    manager.update(
        1,
        "ENTRY"
    )
)

print(
    manager.update(
        1,
        "ENTRY"
    )
)

print(
    manager.update(
        1,
        "SKINCARE"
    )
)

print(
    manager.update(
        1,
        "BILLING"
    )
)