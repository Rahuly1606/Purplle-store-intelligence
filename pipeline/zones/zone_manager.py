from typing import Dict


class ZoneManager:

    def __init__(self):

        self.zones: Dict[str, tuple] = {

            "ENTRY": (
                0,
                0,
                300,
                300
            ),

            "SKINCARE": (
                301,
                0,
                700,
                500
            ),

            "BILLING": (
                701,
                0,
                1200,
                500
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