from ultralytics import YOLO


class PersonDetector:

    def __init__(
        self,
        model_path="yolov8n.pt"
    ):
        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(
            frame,
            classes=[0],
            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                )

                detections.append({
                    "bbox": [
                        float(x1),
                        float(y1),
                        float(x2),
                        float(y2)
                    ],
                    "confidence":
                        float(box.conf[0])
                })

        return detections