MIN_ZONE_DWELL = 2


class StateManager:

    def __init__(self):

        self.track_states = {}

        self.seen_tracks = set()

        self.track_age = {}

        self.confirmed_tracks = set()

        self.zone_entry_time = {}

        self.min_frames_for_entry = 5

    def update(
        self,
        track_id,
        current_zone,
        current_time=0
    ):

        events = []

        # age counter

        self.track_age[
            track_id
        ] = (
            self.track_age.get(
                track_id,
                0
            ) + 1
        )

        # confirm visitor only after N frames

        if (
            track_id
            not in self.confirmed_tracks
        ):

            if (
                self.track_age[
                    track_id
                ]
                >=
                self.min_frames_for_entry
            ):

                self.confirmed_tracks.add(
                    track_id
                )
                self.seen_tracks.add(
                    track_id
                )

                self.track_states[
                    track_id
                ] = current_zone

                self.zone_entry_time[
                    track_id
                ] = current_time

                if current_zone is not None:

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

        time_in_zone = (
            current_time
            - self.zone_entry_time.get(
                track_id,
                current_time
            )
        )

        if previous_zone != current_zone:

            if (
                previous_zone is not None
                and
                time_in_zone < MIN_ZONE_DWELL
            ):
                return events

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

            self.zone_entry_time[
                track_id
            ] = current_time

        return events
    def total_visitors(self):

        return len(
            self.seen_tracks
        )