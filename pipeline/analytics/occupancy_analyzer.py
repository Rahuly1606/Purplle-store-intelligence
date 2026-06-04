class OccupancyAnalyzer:

    def __init__(self):

        self.current_occupancy = {}

        self.peak_occupancy = {}

    def enter_zone(
        self,
        visitor_id,
        zone_id
    ):

        if zone_id is None:
            return

        self.current_occupancy[
            zone_id
        ] = (
            self.current_occupancy.get(
                zone_id,
                0
            ) + 1
        )

        if (
            self.current_occupancy[zone_id]
            >
            self.peak_occupancy.get(
                zone_id,
                0
            )
        ):

            self.peak_occupancy[
                zone_id
            ] = self.current_occupancy[zone_id]

    def exit_zone(
        self,
        visitor_id,
        zone_id
    ):

        if zone_id is None:
            return

        current = self.current_occupancy.get(
            zone_id,
            0
        )

        if current > 0:

            self.current_occupancy[
                zone_id
            ] = current - 1

    def get_metrics(self):

        return dict(self.peak_occupancy)
