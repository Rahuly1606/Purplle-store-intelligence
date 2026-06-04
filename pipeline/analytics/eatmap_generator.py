import cv2
import numpy as np


class HeatmapGenerator:

    def __init__(self):

        self.points = []

    def add_point(
        self,
        x,
        y
    ):

        self.points.append(
            (int(x), int(y))
        )

    def generate(
        self,
        width,
        height,
        output_path
    ):

        heatmap = np.zeros(
            (height, width),
            dtype=np.float32
        )

        for x, y in self.points:

            cv2.circle(
                heatmap,
                (x, y),
                40,
                1,
                -1
            )

        heatmap = cv2.GaussianBlur(
            heatmap,
            (0, 0),
            25
        )

        heatmap = cv2.normalize(
            heatmap,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        heatmap = heatmap.astype(
            np.uint8
        )

        colored = cv2.applyColorMap(
            heatmap,
            cv2.COLORMAP_JET
        )

        cv2.imwrite(
            output_path,
            colored
        )