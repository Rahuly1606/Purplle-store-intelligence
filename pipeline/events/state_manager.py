class StateManager:

    def __init__(self):

        self.track_states = {}

    def update(
        self,
        track_id,
        current_zone
    ):

        events = []

        previous_zone = self.track_states.get(
            track_id
        )

        # First appearance
        if previous_zone is None:

            self.track_states[
                track_id
            ] = current_zone

            if current_zone == "ENTRY":

                events.append(
                    (
                        "ENTRY",
                        current_zone
                    )
                )

            return events

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