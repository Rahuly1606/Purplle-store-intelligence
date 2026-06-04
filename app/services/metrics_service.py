import json


class MetricsService:

    @staticmethod
    def calculate(events):

        visitors = set()
        staff_ids = set()

        converted = set()

        zone_dwells = {}

        queue_depth = 0
        queue_abandons = 0
        queue_joins = 0

        for event in events:

            if event.event_type == "ENTRY":

                visitors.add(event.visitor_id)

                if event.is_staff:
                    staff_ids.add(event.visitor_id)

            elif event.event_type == "BILLING_QUEUE_JOIN":

                converted.add(event.visitor_id)

                queue_joins += 1

                metadata = json.loads(
                    event.metadata_json
                )

                queue_depth = metadata.get(
                    "queue_depth",
                    queue_depth
                )

            elif event.event_type == "BILLING_QUEUE_ABANDON":

                queue_abandons += 1

            elif event.event_type == "ZONE_DWELL":

                if event.zone_id not in zone_dwells:
                    zone_dwells[event.zone_id] = []

                zone_dwells[event.zone_id].append(
                    event.dwell_ms
                )

        real_visitors = visitors - staff_ids

        avg_dwell = {}

        for zone, values in zone_dwells.items():

            avg_dwell[zone] = int(
                sum(values) / len(values)
            )

        conversion_rate = 0.0

        if len(real_visitors) > 0:

            conversion_rate = (
                len(converted)
                / len(real_visitors)
            )

        abandonment_rate = 0.0

        if queue_joins > 0:

            abandonment_rate = (
                queue_abandons
                / queue_joins
            )

        return {
            "unique_visitors": len(real_visitors),

            "conversion_rate": round(
                conversion_rate,
                4
            ),

            "avg_dwell_per_zone_ms": avg_dwell,

            "queue_depth": queue_depth,

            "abandonment_rate": round(
                abandonment_rate,
                4
            )
        }