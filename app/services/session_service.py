from collections import defaultdict


class SessionService:

    @staticmethod
    def build_sessions(events):

        sessions = defaultdict(
            lambda: {
                "visitor_id": None,
                "entered": False,
                "zones": set(),
                "billing": False,
                "converted": False,
                "staff": False
            }
        )

        for event in events:

            visitor_id = event.visitor_id

            session = sessions[visitor_id]

            session["visitor_id"] = visitor_id

            if event.is_staff:
                session["staff"] = True

            if event.event_type in [
                "ENTRY",
                "REENTRY"
            ]:
                session["entered"] = True

            elif event.event_type == "ZONE_ENTER":

                if event.zone_id:
                    session["zones"].add(
                        event.zone_id
                    )

            elif event.event_type == "BILLING_QUEUE_JOIN":

                session["billing"] = True

                session["converted"] = True

        return sessions