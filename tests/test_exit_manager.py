import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.events.exit_manager import (
    ExitManager
)

manager = ExitManager(
    max_missing_frames=5
)

for frame in range(1, 15):

    if frame <= 3:

        active = [1]

    else:

        active = []

    exits = manager.update(
        active,
        frame
    )

    print(
        frame,
        exits
    )