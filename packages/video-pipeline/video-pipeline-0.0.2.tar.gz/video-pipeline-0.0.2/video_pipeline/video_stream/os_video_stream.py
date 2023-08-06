import logging

from typing import Any
from typing import Tuple

import imageio
import numpy as np

from video_pipeline.video_stream import VideoStream

_logger = logging.getLogger(__name__)


# TODO@nw: Add tests...
class OsVideoStream(VideoStream):
    # TODO@nw: Unable to get typing to work for `imageio.core.format.Reader`
    _stream_reader: Any
    _resolution: Tuple[int, int]
    _video_source: str
    _video_format: str

    def __init__(
        self,
        framerate: int,
        resolution: Tuple[int, int],
        *,
        video_format: str = 'FFMPEG',
        video_source: str = '<video0>',
    ) -> None:
        super().__init__(framerate=framerate)
        # TODO@nw: Allow different formats.
        self._resolution = resolution
        self._video_source = video_source
        self._video_format = video_format

    def _start_stream(self) -> None:
        self._stream_reader = imageio.get_reader(
            self._video_source,
            format=self._video_format,
            size=self._resolution,
            mode='?',
            fps=self._framerate
        )

    def _stop_stream(self) -> None:
        self._stream_reader.close()

    def _read_frame(self) -> np.array:
        image_data = self._stream_reader.get_next_data()
        return image_data
