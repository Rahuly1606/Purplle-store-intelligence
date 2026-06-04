class ExitManager:

    def __init__(
        self,
        timeout_seconds=10
    ):

        self.timeout_seconds = (
            timeout_seconds
        )

        self.last_seen = {}

    def update(
        self,
        active_track_ids,
        current_time
    ):

        exits = []

        # update visible tracks

        for track_id in active_track_ids:

            self.last_seen[
                track_id
            ] = current_time

        # find disappeared tracks

        for track_id in list(
            self.last_seen.keys()
        ):

            gap = (
                current_time
                -
                self.last_seen[
                    track_id
                ]
            )

            if (
                gap >
                self.timeout_seconds
            ):

                exits.append(
                    track_id
                )

                del self.last_seen[
                    track_id
                ]

        return exits