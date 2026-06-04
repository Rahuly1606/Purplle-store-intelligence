import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.tracking.tracker import CentroidTracker


def main():

    tracker = CentroidTracker()

    detections = [
        {
            "bbox": [10, 10, 50, 50],
            "confidence": 0.9
        }
    ]

    result = tracker.update(detections)

    print(result)


if __name__ == "__main__":
    main()