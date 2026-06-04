class PathAnalyzer:

    def __init__(self):

        self.paths = {}

    def record_zone(
        self,
        visitor_id,
        zone_id
    ):

        if visitor_id not in self.paths:
            self.paths[visitor_id] = []

        path = self.paths[visitor_id]

        if not path or path[-1] != zone_id:
            path.append(zone_id)

    def get_path(
        self,
        visitor_id
    ):

        return self.paths.get(
            visitor_id,
            []
        )

    def get_all_paths(self):

        return {
            v: list(p)
            for v, p in self.paths.items()
        }
