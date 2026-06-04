import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import cv2

from pipeline.zones.zone_manager import ZoneManager

VIDEO_PATH = "data/videos/sample.mp4"

OUTPUT_IMAGE = "output/zones_debug.jpg"


def main():

    zone_manager = ZoneManager()

    cap = cv2.VideoCapture(
        VIDEO_PATH
    )

    success, frame = cap.read()

    if not success:

        print(
            "Could not read video"
        )

        return

    for zone_name, (
        x1,
        y1,
        x2,
        y2
    ) in zone_manager.zones.items():

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            zone_name,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imwrite(
        OUTPUT_IMAGE,
        frame
    )

    print(
        f"Saved -> {OUTPUT_IMAGE}"
    )

    cap.release()


if __name__ == "__main__":
    main()