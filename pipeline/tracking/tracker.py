class CentroidTracker:
    """
    Simple tracker for initial development.

    This will later be replaced with ByteTrack or DeepSORT.
    For now it simply assigns a unique track_id to each detection.
    """

    def __init__(self):
        self.next_id = 1
        self.objects = {}

    def update(self, detections):
        tracked = []

        for detection in detections:

            if "track_id" not in detection:

                detection["track_id"] = self.next_id

                self.objects[self.next_id] = detection

                self.next_id += 1

            tracked.append(detection)

        return tracked