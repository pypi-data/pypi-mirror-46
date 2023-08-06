import numpy as np
from video_pipeline.frame_filter import FrameFilter
# from skimage.filters import roberts


class FindEdgesFrameFilter(FrameFilter):
    """Based on the scikit-image documentation for
    [edges](https://scikit-image.org/docs/dev/auto_examples/edges/plot_edge_filter.html).
    """

    def process_frame(self, frame: np.array) -> np.array:
        # TODO@nw: Should allow for configuration of different types of edge detection.
        # TODO@nw: Implement...
        # new_frame = roberts(frame)
        return frame
