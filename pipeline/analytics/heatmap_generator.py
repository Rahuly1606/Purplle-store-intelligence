import numpy as np
import cv2


class HeatmapGenerator:

    def __init__(self):

        self.points = []

    def add_point(
        self,
        x,
        y
    ):

        self.points.append((x, y))

    def generate(
        self,
        width,
        height,
        output_path
    ):

        if not self.points:
            return

        heatmap = np.zeros(
            (height, width),
            dtype=np.float32
        )

        for x, y in self.points:

            if (
                0 <= x < width
                and 0 <= y < height
            ):

                heatmap[y, x] += 1

        heatmap = cv2.GaussianBlur(
            heatmap,
            (51, 51),
            0
        )

        max_val = heatmap.max()

        if max_val > 0:
            heatmap /= max_val

        heatmap_uint8 = (
            heatmap * 255
        ).astype(np.uint8)

        colored = cv2.applyColorMap(
            heatmap_uint8,
            cv2.COLORMAP_JET
        )

        cv2.imwrite(
            output_path,
            colored
        )
