import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import cv2

from pipeline.detection.detector import PersonDetector

from pipeline.zones.zone_manager import ZoneManager
from pipeline.zones.hysteresis_manager import HysteresisManager

from pipeline.events.state_manager import StateManager
from pipeline.events.exit_manager import ExitManager

from pipeline.events.event_builder import EventBuilder
from pipeline.events.emitter import EventEmitter

from pipeline.analytics.dwell_engine import DwellEngine


VIDEO_PATH = "data/videos/sample.mp4"

STORE_ID = "STORE_BLR_001"

CAMERA_ID = "CAM_ENTRY_01"

OUTPUT_FILE = "data/events/generated_events.jsonl"

FPS = 30


def get_center(bbox):

    x1, y1, x2, y2 = bbox

    center_x = int((x1 + x2) / 2)

    center_y = int((y1 + y2) / 2)

    return center_x, center_y


def main():

    detector = PersonDetector()

    zone_manager = ZoneManager()

    hysteresis = HysteresisManager(
        threshold=3
    )

    state_manager = StateManager()

    dwell_engine = DwellEngine()

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

        current_time = (
            frame_count / FPS
        )

        tracked = detector.track(
            frame
        )

        active_track_ids = []

        for person in tracked:

            track_id = person["track_id"]

            active_track_ids.append(
                track_id
            )

            bbox = person["bbox"]

            center_x, center_y = (
                get_center(
                    bbox
                )
            )

            raw_zone = (
                zone_manager.get_zone(
                    center_x,
                    center_y
                )
            )

            zone = (
                hysteresis.update(
                    track_id,
                    raw_zone
                )
            )

            print(
                f"TRACK={track_id} "
                f"CENTER=({center_x},{center_y}) "
                f"ZONE={zone}"
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

                # ENTRY starts dwell

                if event_type == "ENTRY":

                    if zone_id is not None:

                        dwell_engine.zone_enter(
                            visitor_id,
                            zone_id,
                            current_time
                        )

                # ZONE ENTER

                elif event_type == "ZONE_ENTER":

                    dwell_engine.zone_enter(
                        visitor_id,
                        zone_id,
                        current_time
                    )

                # ZONE EXIT

                elif event_type == "ZONE_EXIT":

                    dwell = (
                        dwell_engine.zone_exit(
                            visitor_id,
                            zone_id,
                            current_time
                        )
                    )

                    if dwell:

                        print(
                            f"DWELL -> "
                            f"{visitor_id} "
                            f"{zone_id} "
                            f"{dwell['dwell_seconds']:.2f}s"
                        )

                event = (
                    EventBuilder.build_event(
                        event_type=event_type,
                        visitor_id=visitor_id,
                        store_id=STORE_ID,
                        camera_id=CAMERA_ID,
                        zone_id=zone_id
                    )
                )

                emitter.emit(
                    event
                )

                print(
                    f"{event_type} -> "
                    f"{visitor_id}"
                )

        # EXIT DETECTION

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

            current_zone = (
                state_manager.track_states.get(
                    track_id
                )
            )

            if current_zone:

                dwell = (
                    dwell_engine.zone_exit(
                        visitor_id,
                        current_zone,
                        current_time
                    )
                )

                if dwell:

                    print(
                        f"FINAL DWELL -> "
                        f"{visitor_id} "
                        f"{current_zone} "
                        f"{dwell['dwell_seconds']:.2f}s"
                    )

            event = (
                EventBuilder.build_event(
                    event_type="EXIT",
                    visitor_id=visitor_id,
                    store_id=STORE_ID,
                    camera_id=CAMERA_ID
                )
            )

            emitter.emit(
                event
            )

            print(
                f"EXIT -> "
                f"{visitor_id}"
            )

        # remove exited tracks from state

        # remove exited tracks from state

        for track_id in exited_tracks:

            state_manager.track_states.pop(
                track_id,
                None
            )

            hysteresis.current_zone.pop(
                track_id,
                None
            )

            hysteresis.candidate_zone.pop(
                track_id,
                None
            )

            hysteresis.candidate_count.pop(
                track_id,
                None
            )

            exit_manager.last_seen.pop(
                track_id,
                None
            )

    # FORCE EXIT FOR ACTIVE TRACKS

    for track_id in list(
        exit_manager.last_seen.keys()
    ):

        visitor_id = (
            f"VIS_{track_id}"
        )

        current_zone = (
            state_manager.track_states.get(
                track_id
            )
        )

        if current_zone:

            dwell = (
                dwell_engine.zone_exit(
                    visitor_id,
                    current_zone,
                    frame_count / FPS
                )
            )

            if dwell:

                print(
                    f"FINAL DWELL -> "
                    f"{visitor_id} "
                    f"{current_zone} "
                    f"{dwell['dwell_seconds']:.2f}s"
                )

        event = (
            EventBuilder.build_event(
                event_type="EXIT",
                visitor_id=visitor_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID
            )
        )

        emitter.emit(
            event
        )

        print(
            f"FORCED EXIT -> "
            f"{visitor_id}"
        )

    cap.release()

    print(
        "\nPipeline completed"
    )

    print(
        "\nAVERAGE DWELL TIMES:"
    )

    for zone_name in (
        dwell_engine.dwell_times
    ):

        avg = (
            dwell_engine.get_zone_average(
                zone_name
            )
        )

        visits = len(
            dwell_engine.dwell_times[
                zone_name
            ]
        )

        print(
            f"{zone_name}: "
            f"{avg:.2f}s "
            f"({visits} visits)"
        )

    print(
        "\nTOTAL VISITORS:",
        len(
            state_manager.seen_tracks
        )
    )


if __name__ == "__main__":
    main()