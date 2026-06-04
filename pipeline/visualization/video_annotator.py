import cv2


class VideoAnnotator:

    def draw(
        self,
        frame,
        bbox,
        visitor_id,
        zone,
        is_staff=False
    ):

        x1, y1, x2, y2 = map(
            int,
            bbox
        )

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        role = (
            "STAFF"
            if is_staff
            else "CUSTOMER"
        )

        label = (
            f"{visitor_id} | "
            f"{role} | "
            f"{zone}"
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        return frame