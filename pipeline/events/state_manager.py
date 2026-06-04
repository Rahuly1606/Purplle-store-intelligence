class StateManager:

    def __init__(self):

        self.track_states = {}

        self.seen_tracks = set()

    def update(
        self,
        track_id,
        current_zone
    ):

        events = []

        # First time seeing this track
        if track_id not in self.seen_tracks:

            self.seen_tracks.add(
                track_id
            )

            self.track_states[
                track_id
            ] = current_zone

            events.append(
                (
                    "ENTRY",
                    current_zone
                )
            )

            return events

        previous_zone = (
            self.track_states.get(
                track_id
            )
        )

        # Zone transition
        if previous_zone != current_zone:

            if previous_zone is not None:

                events.append(
                    (
                        "ZONE_EXIT",
                        previous_zone
                    )
                )

            if current_zone is not None:

                events.append(
                    (
                        "ZONE_ENTER",
                        current_zone
                    )
                )

            self.track_states[
                track_id
            ] = current_zone

        return events