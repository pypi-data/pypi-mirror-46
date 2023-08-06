import abc
import logging
from types import TracebackType
from typing import Optional
from typing import Tuple
from typing import Type

import numpy as np

from video_pipeline.video_performance import FpsCounter

_logger = logging.getLogger(__name__)


def parse_resolution(resolution: str) -> Tuple[int, int]:
    """Parse a resolution from string format '380x420'."""
    try:
        res = resolution.lower().split('x')
        width = int(res[0])
        height = int(res[1])
    except Exception:
        raise ValueError(f'Unable to parse provided resolution "{resolution}".')

    return (width, height)


class VideoStream(abc.ABC):
    """Abstract base VideoStream that defines the general structure of a VideoStream implementations.

    Should not be instantiated.
    """
    _is_running: bool
    _fps_counter: FpsCounter
    _framerate: int

    def __init__(
        self,
        framerate: int
    ) -> None:
        self._is_running = False
        self._fps_counter = FpsCounter(framerate // 3)
        self._framerate = framerate

    def start(self) -> None:
        """Start up the video stream and start collecting frames.
        """
        if self._is_running:
            raise ValueError('Video stream is already started.')

        self._start_stream()
        self._is_running = True
        self._fps_counter.reset()

    def stop(self) -> None:
        """Close out the video stream.
        """
        if not self._is_running:
            raise ValueError(f'Video stream is already stopped.')

        self._stop_stream()
        self._is_running = False
        self._fps_counter.clear()

    def is_running(self) -> bool:
        return self._is_running

    def read(self) -> np.array:
        """Read the next frame.
        """
        frame = self._read_frame()
        self._fps_counter.count()
        return frame

    def get_fps(self) -> int:
        return self._fps_counter.fps()

    @abc.abstractmethod
    def _start_stream(self) -> None:
        """Start implementation.
        """
        pass

    @abc.abstractmethod
    def _stop_stream(self) -> None:
        """Stop implementation.
        """
        pass

    @abc.abstractmethod
    def _read_frame(self) -> np.array:
        """Read implementation.
        """
        pass

    def __enter__(self) -> 'VideoStream':
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
