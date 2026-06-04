from ultralytics import YOLO


class PersonDetector:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")

    def track(self, frame):

        results = self.model.track(
            frame,
            classes=[0],
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.25,
            iou=0.5,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes.id is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            ids = result.boxes.id.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()

            for box, track_id, conf in zip(
                boxes,
                ids,
                confs
            ):

                if conf < 0.40:
                    continue

                x1, y1, x2, y2 = box

                detections.append({
                    "track_id": int(track_id),
                    "bbox": [
                        float(x1),
                        float(y1),
                        float(x2),
                        float(y2)
                    ],
                    "confidence": float(conf)
                })

        return detections