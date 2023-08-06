import abc
from types import TracebackType
from typing import Optional
from typing import Type

import numpy as np


class VideoTransport(abc.ABC):
    """Abstract base VideoTransport that defines the general structure of
    a VideoTransport implementations.

    Should not be instantiated.
    """
    _is_running: bool

    def __init__(self) -> None:
        self._is_running = False

    def start(self) -> None:
        """Start up the video transport.
        """
        if self._is_running:
            raise ValueError('Video transport is already started.')

        self._start_transport()
        self._is_running = True

    def stop(self) -> None:
        """Close out the video transport.
        """
        if not self._is_running:
            raise ValueError('Video transport is already stopped.')

        self._stop_transport()
        self._is_running = False

    def is_running(self) -> bool:
        return self._is_running

    def transport(self, frame: np.array) -> None:
        return self._transport_frame(frame)

    @abc.abstractmethod
    def _start_transport(self) -> None:
        """Start implementation.
        """
        pass

    @abc.abstractmethod
    def _stop_transport(self) -> None:
        """Stop implementation.
        """
        pass

    @abc.abstractmethod
    def _transport_frame(self, frame: np.array) -> None:
        """Transport implementation.
        """
        pass

    def __enter__(self) -> 'VideoTransport':
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType]
    ) -> None:
        self.stop()
