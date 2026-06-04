import json
from pathlib import Path


CONFIG_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent
    / "config"
    / "zones.json"
)


class ZoneManager:

    def __init__(self):

        with open(CONFIG_PATH) as f:
            data = json.load(f)

        self.zones = {
            name: tuple(coords)
            for name, coords
            in data["zones"].items()
        }

    def get_zone(
        self,
        center_x,
        center_y
    ):

        for zone_name, (
            x1,
            y1,
            x2,
            y2
        ) in self.zones.items():

            if (
                x1 <= center_x <= x2
                and
                y1 <= center_y <= y2
            ):
                return zone_name

        return None
