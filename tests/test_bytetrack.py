import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import cv2

from pipeline.detection.detector import PersonDetector


VIDEO_PATH = "data/videos/sample.mp4"


detector = PersonDetector()

cap = cv2.VideoCapture(
    VIDEO_PATH
)

frame_no = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_no += 1

    if frame_no % 30 != 0:
        continue

    detections = detector.track(
        frame
    )

    print(
        f"\nFRAME {frame_no}"
    )

    for d in detections:

        print(
            f"ID={d['track_id']}"
        )

cap.release()