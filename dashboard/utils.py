import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def load_json(relative_path):
    path = BASE / relative_path
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def get_image_path(relative_path):
    path = BASE / relative_path
    return str(path) if path.exists() else None


def get_video_path(relative_path):
    path = BASE / relative_path
    return str(path) if path.exists() else None
