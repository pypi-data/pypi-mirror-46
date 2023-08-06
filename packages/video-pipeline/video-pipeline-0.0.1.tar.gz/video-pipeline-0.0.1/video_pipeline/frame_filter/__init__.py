import abc

import numpy as np


class FrameFilter(abc.ABC):
    """Abstract base frame filter. Provides the basic structure
    for manipulating frames.

    Should not be directly instantiated.
    """

    def run(self, frame: np.array) -> np.array:
        """Runs the 'process_frame' implementation for this FrameFilter.
        """
        # Process.
        processed_frame = self.process_frame(frame)

        # Make sure we have a processed frame.
        if processed_frame is None:
            raise ValueError(
                f'Received no image frame. Make sure you are returning a frame in "process_frame" for "{type(self).__name__}"'  # noqa: E501
            )

        return processed_frame

    @abc.abstractmethod
    def process_frame(self, frame: np.array) -> np.array:
        raise NotImplementedError


class NoOpFrameFilter(FrameFilter):
    def process_frame(self, frame: np.array) -> np.array:
        return frame
