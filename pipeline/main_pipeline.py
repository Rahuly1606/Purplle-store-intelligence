import sys
import json
import math
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
from pipeline.analytics.staff_classifier import StaffClassifier
from pipeline.analytics.path_analyzer import PathAnalyzer
from pipeline.analytics.funnel_analyzer import FunnelAnalyzer
from pipeline.analytics.occupancy_analyzer import OccupancyAnalyzer
from pipeline.analytics.heatmap_generator import HeatmapGenerator
from pipeline.visualization.video_annotator import VideoAnnotator
from pipeline.reporting.final_report_generator import FinalReportGenerator


VIDEO_PATH = "data/videos/sample.mp4"

STORE_ID = "STORE_BLR_001"

CAMERA_ID = "CAM_ENTRY_01"

OUTPUT_FILE = "data/events/generated_events.jsonl"

METRICS_FILE = "outputs/store_metrics.json"

FPS = 30

REID_DISTANCE = 100

REID_TIME_GAP = 2


def get_feet_point(bbox):

    x1, y1, x2, y2 = bbox

    feet_x = int((x1 + x2) / 2)

    feet_y = int(y2)

    return feet_x, feet_y


def find_reid_match(
    feet_x,
    feet_y,
    current_time,
    recently_lost
):

    for (
        lost_track_id,
        (lx, ly, lost_time)
    ) in recently_lost.items():

        dist = math.hypot(
            feet_x - lx,
            feet_y - ly
        )

        time_gap = current_time - lost_time

        if (
            dist < REID_DISTANCE
            and time_gap < REID_TIME_GAP
        ):
            return lost_track_id

    return None


def main():

    detector = PersonDetector()

    annotator = VideoAnnotator()

    report_generator = (
        FinalReportGenerator()
    )

    zone_manager = ZoneManager()

    hysteresis = HysteresisManager(
        threshold=6
    )

    state_manager = StateManager()

    dwell_engine = DwellEngine()

    occupancy_analyzer = OccupancyAnalyzer()

    heatmap_generator = HeatmapGenerator()

    staff_classifier = StaffClassifier()

    path_analyzer = PathAnalyzer()

    funnel_analyzer = FunnelAnalyzer()

    exit_manager = ExitManager(
        timeout_seconds=10
    )

    emitter = EventEmitter(
        OUTPUT_FILE
    )

    cap = cv2.VideoCapture(
        VIDEO_PATH
    )

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    writer = cv2.VideoWriter(
        "outputs/annotated_store_video.mp4",
        cv2.VideoWriter_fourcc(
            *"mp4v"
        ),
        30,
        (width, height)
    )

    frame_count = 0

    # track_id -> canonical visitor_id (for Re-ID)
    track_to_visitor = {}

    # track_id -> (feet_x, feet_y, last_seen_time)
    recently_lost = {}

    last_positions = {}

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

            bbox = person["bbox"]

            if person["confidence"] < 0.5:
                continue

            bbox_area = (
                (bbox[2] - bbox[0])
                *
                (bbox[3] - bbox[1])
            )

            if bbox_area < 5000:
                continue

            active_track_ids.append(
                track_id
            )

            feet_x, feet_y = (
                get_feet_point(
                    bbox
                )
            )

            heatmap_generator.add_point(
                feet_x,
                feet_y
            )

            last_positions[track_id] = (
                feet_x,
                feet_y
            )

            # Re-ID: reuse visitor_id if recently lost nearby
            if track_id not in track_to_visitor:

                matched = find_reid_match(
                    feet_x,
                    feet_y,
                    current_time,
                    recently_lost
                )

                if matched is not None:

                    track_to_visitor[track_id] = (
                        track_to_visitor.get(
                            matched,
                            f"VIS_{matched}"
                        )
                    )

                    recently_lost.pop(
                        matched,
                        None
                    )

                else:

                    track_to_visitor[track_id] = (
                        f"VIS_{track_id}"
                    )

            visitor_id = track_to_visitor[track_id]

            raw_zone = (
                zone_manager.get_zone(
                    feet_x,
                    feet_y
                )
            )

            zone = (
                hysteresis.update(
                    track_id,
                    raw_zone
                )
            )

            is_staff = (
                staff_classifier.is_staff(
                    visitor_id
                )
            )

            annotator.draw(
                frame,
                bbox,
                visitor_id,
                zone,
                is_staff
            )

            print(
                f"TRACK={track_id} "
                f"VIS={visitor_id} "
                f"FEET=({feet_x},{feet_y}) "
                f"ZONE={zone}"
            )

            state_events = (
                state_manager.update(
                    track_id,
                    zone,
                    current_time
                )
            )

            for (
                event_type,
                zone_id
            ) in state_events:

                if event_type == "ENTRY":

                    if zone_id is not None:

                        dwell_engine.zone_enter(
                            visitor_id,
                            zone_id,
                            current_time
                        )

                        occupancy_analyzer.enter_zone(
                            visitor_id,
                            zone_id
                        )

                        path_analyzer.record_zone(
                            visitor_id,
                            zone_id
                        )

                        funnel_analyzer.record_visit(
                            visitor_id,
                            zone_id
                        )

                elif event_type == "ZONE_ENTER":

                    dwell_engine.zone_enter(
                        visitor_id,
                        zone_id,
                        current_time
                    )

                    occupancy_analyzer.enter_zone(
                        visitor_id,
                        zone_id
                    )

                    path_analyzer.record_zone(
                        visitor_id,
                        zone_id
                    )

                    funnel_analyzer.record_visit(
                        visitor_id,
                        zone_id
                    )

                elif event_type == "ZONE_EXIT":

                    occupancy_analyzer.exit_zone(
                        visitor_id,
                        zone_id
                    )

                    dwell = (
                        dwell_engine.zone_exit(
                            visitor_id,
                            zone_id,
                            current_time
                        )
                    )

                    if dwell:

                        staff_classifier.record_dwell(
                            visitor_id,
                            dwell["dwell_seconds"]
                        )

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

        # write annotated frame
        writer.write(
            frame
        )

        # EXIT DETECTION

        exited_tracks = (
            exit_manager.update(
                active_track_ids,
                current_time
            )
        )

        for track_id in exited_tracks:

            if track_id not in state_manager.seen_tracks:
                recently_lost.pop(track_id, None)
                continue

            visitor_id = track_to_visitor.get(
                track_id,
                f"VIS_{track_id}"
            )

            current_zone = (
                state_manager.track_states.get(
                    track_id
                )
            )

            if current_zone:

                occupancy_analyzer.exit_zone(
                    visitor_id,
                    current_zone
                )

                dwell = (
                    dwell_engine.zone_exit(
                        visitor_id,
                        current_zone,
                        current_time
                    )
                )

                if dwell:

                    staff_classifier.record_dwell(
                        visitor_id,
                        dwell["dwell_seconds"]
                    )

                    print(
                        f"FINAL DWELL -> "
                        f"{visitor_id} "
                        f"{current_zone} "
                        f"{dwell['dwell_seconds']:.2f}s"
                    )

            # store last position for Re-ID
            if track_id in last_positions:

                x, y = last_positions[track_id]

                recently_lost[track_id] = (
                    x,
                    y,
                    current_time
                )

        # remove exited tracks from state

        for track_id in exited_tracks:

            state_manager.track_states.pop(
                track_id,
                None
            )

            state_manager.confirmed_tracks.discard(
                track_id
            )

            state_manager.track_age.pop(
                track_id,
                None
            )

            hysteresis.remove_track(
                track_id
            )

            exit_manager.last_seen.pop(
                track_id,
                None
            )

    cap.release()

    writer.release()

    heatmap_generator.generate(
        width=1920,
        height=1080,
        output_path="outputs/heatmap.png"
    )

    print(
        "\nPipeline completed"
    )

    # staff filtering

    customers = staff_classifier.get_customers()

    all_visitors = state_manager.seen_tracks

    staff_ids = {
        track_to_visitor.get(t, f"VIS_{t}")
        for t in all_visitors
        if track_to_visitor.get(
            t, f"VIS_{t}"
        ) not in customers
        and track_to_visitor.get(
            t, f"VIS_{t}"
        ) in staff_classifier.visitor_total_dwell
    }

    print(
        "\nAVERAGE DWELL TIMES:"
    )

    avg_dwell = {}

    zone_visits = {}

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

        avg_dwell[zone_name] = round(avg, 2)

        zone_visits[zone_name] = visits

        print(
            f"{zone_name}: "
            f"{avg:.2f}s "
            f"({visits} visits)"
        )

    total_visitors = state_manager.total_visitors()

    print(
        "\nTOTAL VISITORS:",
        total_visitors
    )

    print(
        "\nVISITOR PATHS:"
    )

    all_paths = path_analyzer.get_all_paths()

    for vis, path in all_paths.items():
        print(f"{vis}: {' -> '.join(path)}")

    funnel = funnel_analyzer.get_funnel()

    print(
        "\nFUNNEL:"
    )

    print(
        funnel
    )

    foh_visitors = set()

    cash_visitors = set()

    for visitor_id, path in all_paths.items():

        if "FOH" in path:
            foh_visitors.add(
                visitor_id
            )

        if "CASH_COUNTER" in path:
            cash_visitors.add(
                visitor_id
            )

    converted = len(
        foh_visitors &
        cash_visitors
    )

    conversion_rate = (
        converted /
        len(foh_visitors)
        if len(foh_visitors) > 0
        else 0
    )

    metrics = {
        "total_visitors": total_visitors,
        "staff_count": len(staff_ids),
        "customer_count": total_visitors - len(staff_ids),
        "avg_dwell_time": avg_dwell,
        "zone_visits": zone_visits,
        "zone_funnel": funnel,
        "peak_occupancy":
            occupancy_analyzer.get_metrics(),
        "conversion_rate": {
            "FOH_TO_CASH_COUNTER": round(
                conversion_rate,
                4
            )
        },
        "visitor_paths": all_paths
    }

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    report_generator.generate(
        metrics,
        "outputs/final_report.json"
    )

    print(
        f"\nMetrics saved to {METRICS_FILE}"
    )


if __name__ == "__main__":
    main()
