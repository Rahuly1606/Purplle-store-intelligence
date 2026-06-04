class HeatmapService:

    @staticmethod
    def calculate(events):

        zone_visits = {}
        zone_dwells = {}

        for event in events:

            if event.is_staff:
                continue

            if event.event_type == "ZONE_ENTER":

                if event.zone_id not in zone_visits:
                    zone_visits[event.zone_id] = set()

                zone_visits[event.zone_id].add(
                    event.visitor_id
                )

            elif event.event_type == "ZONE_DWELL":

                if event.zone_id not in zone_dwells:
                    zone_dwells[event.zone_id] = []

                zone_dwells[event.zone_id].append(
                    event.dwell_ms
                )

        visit_counts = {}

        for zone, visitors in zone_visits.items():
            visit_counts[zone] = len(visitors)

        avg_dwell = {}

        for zone, dwell_values in zone_dwells.items():

            avg_dwell[zone] = int(
                sum(dwell_values) /
                len(dwell_values)
            )

        max_visit = max(
            visit_counts.values(),
            default=1
        )

        normalized_intensity = {}

        for zone, count in visit_counts.items():

            normalized_intensity[zone] = round(
                (count / max_visit) * 100,
                2
            )

        return {
            "zone_visits": visit_counts,
            "zone_dwell_avg_ms": avg_dwell,
            "normalized_intensity": normalized_intensity
        }