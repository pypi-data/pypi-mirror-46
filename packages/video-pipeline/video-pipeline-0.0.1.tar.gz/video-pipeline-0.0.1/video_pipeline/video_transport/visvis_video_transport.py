from typing import Tuple
from typing import Optional

import numpy as np
import visvis as vv

from video_pipeline.video_transport import VideoTransport


class VisVisVideoTransport(VideoTransport):
    _starting_window_resolution: Tuple[int, int]
    _vis_window: Optional[vv.Texture2D]

    def __init__(
        self,
        *,
        starting_window_resolution: Tuple[int, int] = (1920, 1080)
    ) -> None:
        super().__init__()

        self._starting_window_resolution = starting_window_resolution
        self._vis_window = None

    def _start_transport(self) -> None:
        self._vis_window = vv.imshow(np.empty(self._starting_window_resolution), clim=(0, 255))

    def _stop_transport(self) -> None:
        if self._vis_window is not None:
            self._vis_window.Destroy()

    def _transport_frame(self, frame: np.array) -> None:
        vv.processEvents()
        if self._vis_window is not None:
            self._vis_window.SetData(frame)
