import abc
import logging
import sys
from types import TracebackType
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Type

from halo import Halo

from video_pipeline.video_processor import VideoProcessor
from video_pipeline.video_stream import VideoStream
from video_pipeline.video_transport import VideoTransport

_logger = logging.getLogger(__name__)


class Metrics(NamedTuple):
    stream_fps: int
    processor_fps: int


def _get_metrics(
    video_stream: VideoStream,
    video_processor: VideoProcessor,
    video_transport: VideoTransport,
) -> Metrics:
    return Metrics(
        stream_fps=video_stream.get_fps(),
        processor_fps=video_processor.get_fps()
    )


class MetricsHandler(abc.ABC):
    def start(self) -> None:
        return self._start()

    def stop(self) -> None:
        return self._stop()

    def perform(
        self,
        video_stream: VideoStream,
        video_processor: VideoProcessor,
        video_transport: VideoTransport,
    ) -> None:
        return self._perform(
            video_stream,
            video_processor,
            video_transport
        )

    @abc.abstractmethod
    def _perform(
        self,
        video_stream: VideoStream,
        video_processor: VideoProcessor,
        video_transport: VideoTransport,
    ) -> None:
        pass

    @abc.abstractmethod
    def _start(self) -> None:
        pass

    @abc.abstractmethod
    def _stop(self) -> None:
        pass

    def __enter__(self) -> 'MetricsHandler':
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType]
    ) -> None:
        self.stop()


class SpinnerMetricsHandler(MetricsHandler):
    def _perform(
        self,
        video_stream: VideoStream,
        video_processor: VideoProcessor,
        video_transport: VideoTransport,
    ) -> None:
        metrics = _get_metrics(video_stream, video_processor, video_transport)
        self._spinner.text = f'[ (VideoStream {metrics.stream_fps}fps) --> (VideoProcessor {metrics.processor_fps}fps) ]'

    def _start(self) -> None:
        self._spinner = Halo(
            text='Waiting for connection...',
            spinner={
                'interval': 160,
                'frames': ['▹▹▹▹', '▸▹▹▹', '▹▸▹▹', '▹▹▸▹', '▹▹▹▸']
            }
        )
        self._spinner.start()

    def _stop(self) -> None:
        self._spinner.stop()


class PipeMetricsHandler(MetricsHandler):
    def _perform(
        self,
        video_stream: VideoStream,
        video_processor: VideoProcessor,
        video_transport: VideoTransport,
    ) -> None:
        metrics = _get_metrics(video_stream, video_processor, video_transport)
        _logger.info(f'{metrics.stream_fps},{metrics.processor_fps}')

    def _start(self) -> None:
        _logger.info('Stream FPS,Processor FPS')

    def _stop(self) -> None:
        pass


# TODO@nw: Add tests...
def get_metrics_handler(config: Dict[str, str]) -> MetricsHandler:
    if not sys.stdout.isatty():
        return PipeMetricsHandler()

    return SpinnerMetricsHandler()
