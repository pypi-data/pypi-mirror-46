import logging
from typing import BinaryIO

import imageio
import numpy as np

from video_pipeline.video_transport import VideoTransport

_logger = logging.getLogger(__name__)


class FileVideoTransport(VideoTransport):
    _file_path: str
    _file: BinaryIO

    def __init__(
        self,
        file_path: str,
        # TODO@nw: Support multiple formats...
        video_format: str = 'JPEG-PIL'
    ) -> None:
        super().__init__()
        self._file_path = file_path
        self._video_format_conversion = video_format

    def _start_transport(self) -> None:
        self._file = open(self._file_path, 'wb')

    def _stop_transport(self) -> None:
        self._file.close()

    def _transport_frame(self, frame: np.array) -> None:
        # The imsave does not provide safe signature types, indicate bytes.
        image_data: bytes = imageio.imsave(
            imageio.RETURN_BYTES,
            frame,
            format=self._video_format_conversion
        )
        self._file.write(image_data)
