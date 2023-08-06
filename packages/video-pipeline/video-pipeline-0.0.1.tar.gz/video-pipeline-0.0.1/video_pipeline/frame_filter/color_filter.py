from typing import Tuple
from video_pipeline.frame_filter import FrameFilter
import numpy as np


class ColorFilterFrameFilter(FrameFilter):
    """Frame filter for filtering an image by a range of colors in HSL colorspace.

    The filter is defined in Hue-Saturation-Value colorspace so as to allow
    selections of similar colors within a continuous range. The range is
    conposed of an upper allowed HLS color and a lower allowed HSV color. Pixels
    whose HSV coordinates fall between the upper and lower bounds will remain
    unchanged, and pixels outside the range will be converted to black. Filter
    values should be within uint8 (0 to 255).

    This assumes that each frame is in 3 channel RGB format. Result is an image
    in RGB format where every pixel that is not within the desired color range
    is set to black.
    """

    def __init__(
        self,
        hsv_lower_limit: Tuple[float, float, float] = (0, 255, 0),
        hsv_upper_limit: Tuple[float, float, float] = (255, 0, 0)
    ) -> None:
        super().__init__()
        self.hsv_lower_limit = hsv_lower_limit
        self.hsv_upper_limit = hsv_upper_limit

    def process_frame(self, image_frame: np.array) -> np.array:
        try:
            # create HSV mask
            import cv2
            hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv_frame, self.hsv_lower_limit, self.hsv_upper_limit)

            # apply HSV mask to image
            filtered_frame = cv2.bitwise_and(image_frame, image_frame, mask=mask)

            return filtered_frame
        except Exception:
            raise
