from enum import Enum
from typing import Tuple

import numpy as np

from video_pipeline.frame_filter import FrameFilter


class HsvErrorCode(Enum):
    HUE = 0
    SATURATION = 1
    VALUE = 2
    MISSING_VALUES = 3


class HsvParseError(Exception):
    def __init__(
        self,
        hsv_input: str,
        parse_error: HsvErrorCode
    ) -> None:
        self.parse_error = parse_error

        # Provide a decent error message.
        error_message = f'Unable to parse provided HSV "{hsv_input}".'
        if HsvErrorCode.HUE == parse_error:
            error_message += f'\n  Hue must be a valid float between 0 and 360 degrees.'
        elif HsvErrorCode.SATURATION == parse_error:
            error_message += f'\n  Saturation must be a valid uint8 between 0 and 255.'
        elif HsvErrorCode.VALUE == parse_error:
            error_message += f'  Value must be a valid uint8, between 0 and 255.'
        elif HsvErrorCode.MISSING_VALUES == parse_error:
            error_message += f'  Not properly formatted. Should have three values separated by commas.'

        super().__init__(error_message)


def parse_hsv(hsv_input: str) -> Tuple[float, int, int]:  # noqa: C901
    """Parse an hsv (Hue, Saturation, Value) from string format '360,255,255'.
    """
    split_hsv = hsv_input.lower().split(',')

    if len(split_hsv) != 3:
        raise HsvParseError(hsv_input, HsvErrorCode.MISSING_VALUES)

    try:
        h = float(split_hsv[0])
    except Exception:
        raise HsvParseError(hsv_input, HsvErrorCode.HUE)

    try:
        s = int(split_hsv[1])
    except Exception:
        raise HsvParseError(hsv_input, HsvErrorCode.SATURATION)

    try:
        v = int(split_hsv[2])
    except Exception:
        raise HsvParseError(hsv_input, HsvErrorCode.VALUE)

    if h < 0 or h > 360:
        raise HsvParseError(hsv_input, HsvErrorCode.HUE)

    if s < 0 or s > 255:
        raise HsvParseError(hsv_input, HsvErrorCode.SATURATION)

    if v < 0 or v > 255:
        raise HsvParseError(hsv_input, HsvErrorCode.VALUE)

    return (h, s, v)


class ColorFilterFrameFilter(FrameFilter):
    """Frame filter for filtering an image by a range of colors in HSL colorspace.

    The filter is defined in Hue-Saturation-Value colorspace so as to allow
    selections of similar colors within a continuous range. The range is
    conposed of an upper allowed HLS color and a lower allowed HSV color. Pixels
    whose HSV coordinates fall between the upper and lower bounds will remain
    unchanged, and pixels outside the range will be converted to black.

    Result is an image in RGB format where every pixel that is not within the
    desired color range is set to black.
    """
    _lower_limit: Tuple[float, int, int]
    _upper_limit: Tuple[float, int, int]

    def __init__(
        self,
        # 0-360°, 0-255, 0-255
        hsv_lower_limit: Tuple[float, int, int],
        hsv_upper_limit: Tuple[float, int, int],
    ) -> None:
        super().__init__()
        self._lower_limit = hsv_lower_limit
        self._upper_limit = hsv_upper_limit

    def process_frame(self, image_frame: np.array) -> np.array:
        # External Dependencies.
        import cv2

        # Process.
        # Create HSV mask.
        hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv_frame, self._lower_limit, self._upper_limit)

        # Apply HSV mask to image.
        filtered_frame = cv2.bitwise_or(image_frame, image_frame, mask=mask)

        return filtered_frame
