from collections import defaultdict


class DwellEngine:

    def __init__(self):

        self.zone_entry_time = {}

        self.dwell_times = defaultdict(list)

    def zone_enter(
        self,
        visitor_id,
        zone_id,
        timestamp
    ):

        self.zone_entry_time[
            (visitor_id, zone_id)
        ] = timestamp

    def zone_exit(
        self,
        visitor_id,
        zone_id,
        timestamp
    ):

        key = (
            visitor_id,
            zone_id
        )

        if key not in self.zone_entry_time:
            return None

        start_time = (
            self.zone_entry_time[key]
        )

        dwell_seconds = (
            timestamp - start_time
        )

        self.dwell_times[
            zone_id
        ].append(
            dwell_seconds
        )

        del self.zone_entry_time[key]

        return {
            "visitor_id": visitor_id,
            "zone_id": zone_id,
            "dwell_seconds": dwell_seconds
        }

    def get_zone_average(
        self,
        zone_id
    ):

        values = self.dwell_times.get(
            zone_id,
            []
        )

        if not values:
            return 0

        return sum(values) / len(values)