from typing import Dict


class ZoneManager:

    def __init__(self):

        self.zones: Dict[str, tuple] = {

            "ENTRY": (
                700,
                550,
                1100,
                950
            ),

            "SKINCARE": (
                1101,
                550,
                1500,
                950
            ),

            "BILLING": (
                1501,
                300,
                1920,
                950
            )
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