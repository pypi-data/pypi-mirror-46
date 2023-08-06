import numpy as np
from video_pipeline.frame_filter import FrameFilter
from skimage.color import rgb2gray
from skimage.filters import roberts


class FindEdgesFrameFilter(FrameFilter):
    """Based on the scikit-image documentation for
    [edges](https://scikit-image.org/docs/dev/auto_examples/edges/plot_edge_filter.html).
    """

    def process_frame(self, frame: np.array) -> np.array:
        # TODO@nw: Should allow for configuration of different types of edge detection.
        gray_scale = rgb2gray(frame)
        new_frame = roberts(gray_scale)

        # rgb2gray provides a float64 img, convert to uint8 to support our protocol.
        normalized_frame = np.divide(new_frame.astype(np.float64), new_frame.max())  # normalize the data to 0 - 1
        scaled_frame = 255 * normalized_frame  # Now scale by 255
        return scaled_frame.astype(np.uint8)
