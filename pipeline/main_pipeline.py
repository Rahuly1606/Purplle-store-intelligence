import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import cv2

from pipeline.detection.detector import PersonDetector
from pipeline.zones.zone_manager import ZoneManager

from pipeline.events.state_manager import StateManager
from pipeline.events.exit_manager import ExitManager

from pipeline.events.event_builder import EventBuilder
from pipeline.events.emitter import EventEmitter


VIDEO_PATH = "data/videos/sample.mp4"

STORE_ID = "STORE_BLR_001"

CAMERA_ID = "CAM_ENTRY_01"

OUTPUT_FILE = "data/events/generated_events.jsonl"


def get_center(bbox):

    x1, y1, x2, y2 = bbox

    center_x = int((x1 + x2) / 2)

    center_y = int((y1 + y2) / 2)

    return center_x, center_y


def main():

    detector = PersonDetector()

    zone_manager = ZoneManager()

    state_manager = StateManager()

    exit_manager = ExitManager(
        max_missing_frames=50
    )

    emitter = EventEmitter(
        OUTPUT_FILE
    )

    cap = cv2.VideoCapture(
        VIDEO_PATH
    )

    frame_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        if frame_count % 10 != 0:
            continue

        tracked = detector.track(
            frame
        )

        active_track_ids = []

        for person in tracked:

            track_id = person[
                "track_id"
            ]

            active_track_ids.append(
                track_id
            )

            bbox = person[
                "bbox"
            ]

            center_x, center_y = (
                get_center(
                    bbox
                )
            )

            zone = (
                zone_manager.get_zone(
                    center_x,
                    center_y
                )
            )

            state_events = (
                state_manager.update(
                    track_id,
                    zone
                )
            )

            for (
                event_type,
                zone_id
            ) in state_events:

                visitor_id = (
                    f"VIS_{track_id}"
                )

                event = (
                    EventBuilder.build_event(
                        event_type=
                            event_type,

                        visitor_id=
                            visitor_id,

                        store_id=
                            STORE_ID,

                        camera_id=
                            CAMERA_ID,

                        zone_id=
                            zone_id
                    )
                )

                emitter.emit(
                    event
                )

                print(
                    f"{event_type}"
                    f" -> "
                    f"{visitor_id}"
                )

        # EXIT detection
        exited_tracks = (
            exit_manager.update(
                active_track_ids,
                frame_count
            )
        )

        for track_id in exited_tracks:

            visitor_id = (
                f"VIS_{track_id}"
            )

            event = (
                EventBuilder.build_event(
                    event_type="EXIT",

                    visitor_id=
                        visitor_id,

                    store_id=
                        STORE_ID,

                    camera_id=
                        CAMERA_ID
                )
            )

            emitter.emit(
                event
            )

            print(
                f"EXIT -> "
                f"{visitor_id}"
            )

    cap.release()

    print(
        "Pipeline completed"
    )


if __name__ == "__main__":
    main()