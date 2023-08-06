
import numpy as np
from queue import Full

from video_pipeline.frame_filter import FrameFilter
from video_pipeline.video_processor import BackPressureError
from video_pipeline.video_processor import VideoProcessor


# TODO@nw: Add tests around serial video processor...
class SerialVideoProcessor(VideoProcessor):
    """
    A video processor that processes frames in serial on the calling thread.

    Arguments:
        frame_buffer_size - The size of the frame buffer of processed frames. (Usually double the video framerate.)
        frame_backlog_size - The max amount of processors to keep running before running into backpressure scenarios.
    """

    def __init__(
        self,
        frame_buffer_size: int = 30,
        frame_backlog_size: int = 15,
    ) -> None:
        super().__init__(
            frame_buffer_size=frame_buffer_size,
            frame_backlog_size=frame_backlog_size
        )

    def _start_processor(self) -> None:
        pass

    def _stop_processor(self) -> None:
        pass

    def _process_frame(self, frame_filter: FrameFilter, frame: np.array) -> None:
        try:
            # Get the processed frame.
            processed_frame = frame_filter.run(frame)

            # Add it to our frame buffer.
            self._frame_buffer.put_nowait(processed_frame)
            self._fps_counter.count()
        except Full:
            raise BackPressureError()
        except Exception:
            raise
