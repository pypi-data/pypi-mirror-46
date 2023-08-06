import abc
from queue import Empty
from queue import Queue
from types import TracebackType
from typing import Optional
from typing import Type

import numpy as np

from video_pipeline.frame_filter import FrameFilter
from video_pipeline.video_performance import FpsCounter


class BackPressureError(Exception):
    def __init__(self) -> None:
        super().__init__('Occurs when frames are unable to be processed.')


class BufferOverflowError(Exception):
    def __init__(self) -> None:
        super().__init__('Occurs when frames are processed over the maximum allocated size of the frame buffer.')


class BufferEmptyError(Exception):
    def __init__(self) -> None:
        super().__init__('Occurs when no frames are present in the frame buffer.')


class VideoProcessor(abc.ABC):
    """
    A supporting module to handle the processing of image frames.

    Arguments:
        frame_buffer_size - The size of the frame buffer of processed frames. (Usually double the video framerate.)
        frame_backlog_size - The max amount of processors to keep running before running into backpressure scenarios.

    Example:
        ```
        with VideoProcessor(process_count=4) as video_processor:
            video_processor.process(frame)
            processed_frame = video_processor.read():
            # Do something with processed frame...
        ```
    """
    _frame_buffer_size: int
    _frame_backlog_size: int
    _read_timeout: int
    _is_running: bool
    _frame_buffer: Queue
    _fps_counter: FpsCounter

    def __init__(
        self,
        frame_buffer_size: int = 30,
        frame_backlog_size: int = 15,
    ) -> None:
        self._frame_buffer_size = frame_buffer_size
        self._frame_backlog_size = frame_backlog_size
        self._read_timeout = 1
        self._is_running = False
        self._frame_buffer = Queue(maxsize=self._frame_buffer_size)
        self._fps_counter = FpsCounter(sample_size=frame_buffer_size // 3)

    def start(self) -> None:
        """Start up the video processor.
        """
        if self._is_running:
            raise ValueError('Video processor is already started.')

        self._fps_counter.reset()
        self._start_processor()
        self._is_running = True

    def stop(self) -> None:
        """Close out the video processor.
        """
        if not self._is_running:
            raise ValueError('Video processor is already stopped.')

        self._stop_processor()
        self._is_running = False
        self._fps_counter.clear()

    def process(self, frame_filter: FrameFilter, frame: np.array) -> None:
        """Setup an frame to be processed with the desired frame filter.

        Arguments:
            frame_filter - The frame filter that holds the logic used to process an image frame.
            frame - Image frame to be processed.
        """
        # TODO@nw: Add tests for processing frames when not running...
        if not self._is_running:
            raise ValueError('Unable to process frame. Video processor is not started.')

        return self._process_frame(frame_filter, frame)

    def read(self) -> np.array:
        """Obtain the next available processed frame.
        """
        try:
            return self._frame_buffer.get(timeout=self._read_timeout)
        except Empty:
            raise BufferEmptyError()

    def get_fps(self) -> int:
        return self._fps_counter.fps()

    @abc.abstractmethod
    def _start_processor(self) -> None:
        pass

    @abc.abstractmethod
    def _stop_processor(self) -> None:
        pass

    @abc.abstractmethod
    def _process_frame(self, frame_filter: FrameFilter, frame: np.array) -> None:
        pass

    def __enter__(self) -> 'VideoProcessor':
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType]
    ) -> None:
        self.stop()

    def __next__(self) -> np.array:
        return self.read()
