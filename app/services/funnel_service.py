class FunnelService:

    @staticmethod
    def calculate(events):

        entries = set()
        zone_visitors = set()
        billing_visitors = set()
        converted_visitors = set()

        for event in events:

            if event.is_staff:
                continue

            if event.event_type == "ENTRY":
                entries.add(event.visitor_id)

            elif event.event_type == "ZONE_ENTER":
                zone_visitors.add(event.visitor_id)

            elif event.event_type == "BILLING_QUEUE_JOIN":

                billing_visitors.add(
                    event.visitor_id
                )

                converted_visitors.add(
                    event.visitor_id
                )

        entry_count = len(entries)
        zone_count = len(zone_visitors)
        billing_count = len(billing_visitors)
        conversion_count = len(converted_visitors)

        return {

            "entry": entry_count,

            "zone_visit": zone_count,

            "billing_queue": billing_count,

            "conversion": conversion_count,

            "entry_pct": 100.0 if entry_count else 0,

            "zone_visit_pct":
                round(
                    (zone_count / entry_count) * 100,
                    2
                )
                if entry_count else 0,

            "billing_queue_pct":
                round(
                    (billing_count / entry_count) * 100,
                    2
                )
                if entry_count else 0,

            "conversion_pct":
                round(
                    (conversion_count / entry_count) * 100,
                    2
                )
                if entry_count else 0
        }