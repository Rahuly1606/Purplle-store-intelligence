class ExitManager:

    def __init__(
        self,
        max_missing_frames=50
    ):

        self.max_missing_frames = (
            max_missing_frames
        )

        self.last_seen = {}

    def update(
        self,
        active_track_ids,
        frame_number
    ):

        exits = []

        # Update currently visible tracks
        for track_id in active_track_ids:

            self.last_seen[
                track_id
            ] = frame_number

        # Detect disappeared tracks
        for track_id in list(
            self.last_seen.keys()
        ):

            gap = (
                frame_number
                -
                self.last_seen[
                    track_id
                ]
            )

            if gap > self.max_missing_frames:

                exits.append(
                    track_id
                )

                del self.last_seen[
                    track_id
                ]

        return exits