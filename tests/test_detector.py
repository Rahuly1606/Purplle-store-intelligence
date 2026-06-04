import sys
from pathlib import Path

# Add project root to path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from pipeline.detection.detector import PersonDetector

detector = PersonDetector()

print("Detector loaded successfully")