class FunnelAnalyzer:

    def __init__(self):

        self.zone_visitors = {}

    def record_visit(
        self,
        visitor_id,
        zone_id
    ):

        if zone_id not in self.zone_visitors:
            self.zone_visitors[zone_id] = set()

        self.zone_visitors[zone_id].add(
            visitor_id
        )

    def get_funnel(self):

        return {
            zone: len(visitors)
            for zone, visitors
            in self.zone_visitors.items()
        }

    def get_conversion(
        self,
        from_zone,
        to_zone
    ):

        from_visitors = (
            self.zone_visitors.get(
                from_zone,
                set()
            )
        )

        to_visitors = (
            self.zone_visitors.get(
                to_zone,
                set()
            )
        )

        if len(from_visitors) == 0:
            return 0.0

        converted = len(
            from_visitors &
            to_visitors
        )

        return round(
            converted /
            len(from_visitors),
            4
        )
