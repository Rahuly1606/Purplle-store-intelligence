class HysteresisManager:

    def __init__(
        self,
        threshold=10
    ):

        self.threshold = threshold

        self.current_zone = {}

        self.candidate_zone = {}

        self.candidate_count = {}

    def update(
        self,
        track_id,
        detected_zone
    ):

        # first observation

        if track_id not in self.current_zone:

            self.current_zone[
                track_id
            ] = detected_zone

            return detected_zone

        current = self.current_zone[
            track_id
        ]

        if detected_zone is None:

            return current

        # no change

        if detected_zone == current:

            self.candidate_zone.pop(
                track_id,
                None
            )

            self.candidate_count.pop(
                track_id,
                None
            )

            return current

        # new candidate zone

        if (
            track_id
            not in self.candidate_zone
        ):

            self.candidate_zone[
                track_id
            ] = detected_zone

            self.candidate_count[
                track_id
            ] = 1

            return current

        # candidate changed again

        if (
            self.candidate_zone[
                track_id
            ] != detected_zone
        ):

            self.candidate_zone[
                track_id
            ] = detected_zone

            self.candidate_count[
                track_id
            ] = 1

            return current

        # same candidate repeated

        self.candidate_count[
            track_id
        ] += 1

        if (
            self.candidate_count[
                track_id
            ]
            >= self.threshold
        ):

            self.current_zone[
                track_id
            ] = detected_zone

            self.candidate_zone.pop(
                track_id,
                None
            )

            self.candidate_count.pop(
                track_id,
                None
            )

            return detected_zone

        return current

    def remove_track(
        self,
        track_id
    ):

        self.current_zone.pop(
            track_id,
            None
        )

        self.candidate_zone.pop(
            track_id,
            None
        )

        self.candidate_count.pop(
            track_id,
            None
        )