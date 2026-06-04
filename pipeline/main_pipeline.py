import sys
from pathlib import Path

# Add project root to path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import cv2

from pipeline.detection.detector import PersonDetector
from pipeline.tracking.tracker import CentroidTracker
from pipeline.events.event_builder import EventBuilder
from pipeline.events.emitter import EventEmitter


VIDEO_PATH = "data/videos/sample.mp4"

STORE_ID = "STORE_BLR_001"

CAMERA_ID = "CAM_ENTRY_01"

OUTPUT_FILE = "data/events/generated_events.jsonl"


def main():

    if not Path(VIDEO_PATH).exists():

        print(
            f"Video not found: {VIDEO_PATH}"
        )

        return

    detector = PersonDetector()

    tracker = CentroidTracker()

    emitter = EventEmitter(
        OUTPUT_FILE
    )

    cap = cv2.VideoCapture(
        VIDEO_PATH
    )

    frame_count = 0

    seen_tracks = set()

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        # Process every 10th frame
        if frame_count % 10 != 0:
            continue

        detections = detector.detect(
            frame
        )

        tracked = tracker.update(
            detections
        )

        for person in tracked:

            track_id = person["track_id"]

            visitor_id = (
                f"VIS_{track_id}"
            )

            if track_id not in seen_tracks:

                seen_tracks.add(
                    track_id
                )

                event = (
                    EventBuilder.entry_event(
                        visitor_id=visitor_id,
                        store_id=STORE_ID,
                        camera_id=CAMERA_ID
                    )
                )

                emitter.emit(event)

                print(
                    f"ENTRY -> {visitor_id}"
                )

    cap.release()

    print(
        "Pipeline completed"
    )


if __name__ == "__main__":
    main()