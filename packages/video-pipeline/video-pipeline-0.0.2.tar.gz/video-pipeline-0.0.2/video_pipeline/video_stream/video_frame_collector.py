import io
import logging
from queue import Full
from queue import Queue

import filetype

_logger = logging.getLogger(__name__)


class VideoFrameCollector:
    """Collects video frames from a buffer queue derived from a byte stream of video.
    """
    _frame_buffer_queue: Queue
    _frame_buffer_stream: io.BytesIO
    _frame_buffer_timeout: int

    def __init__(self, maxsize: int) -> None:
        self._frame_buffer_queue = Queue(maxsize=maxsize)
        self._frame_buffer_stream = io.BytesIO()
        self._frame_buffer_read_timeout = 3
        self._frame_buffer_write_timeout = 1

    def write(self, video_buffer: bytes) -> None:
        # Start of new image frame?
        if filetype.image(video_buffer):
            # Make sure we have data in the stream.
            if self._frame_buffer_stream.tell() > 0:
                # Read in the old frame.
                # Wrap in try/finally for stream misgivings.
                try:
                    self._frame_buffer_stream.seek(0)
                    frame = self._frame_buffer_stream.getvalue()

                    # Append frame to buffer.
                    # TODO@nw: Instead of dropping the latest frame we need to be sampling instead.
                    self._frame_buffer_queue.put(
                        frame,
                        timeout=self._frame_buffer_write_timeout
                    )
                except Full:
                    pass
                finally:
                    # Reset the stream and read event.
                    # Allows us to write the new frame.
                    self._frame_buffer_stream.seek(0)
                    self._frame_buffer_stream.truncate()

        # Write to the current frame buffer.
        self._frame_buffer_stream.write(video_buffer)

    def get_next(self) -> bytes:
        frame: bytes = self._frame_buffer_queue.get(
            timeout=self._frame_buffer_read_timeout
        )
        return frame
