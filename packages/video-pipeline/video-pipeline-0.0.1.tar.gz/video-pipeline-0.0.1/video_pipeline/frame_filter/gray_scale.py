from video_pipeline.frame_filter import FrameFilter
import numpy as np
from skimage.color import rgb2gray


class GrayScaleFrameFilter(FrameFilter):
    def process_frame(self, frame: np.array) -> np.array:
        new_frame = rgb2gray(frame)

        # rgb2gray provides a float64 img, convert to uint8 to support our protocol.
        normalized_frame = np.divide(new_frame.astype(np.float64), new_frame.max())  # normalize the data to 0 - 1
        scaled_frame = 255 * normalized_frame  # Now scale by 255
        return scaled_frame.astype(np.uint8)
