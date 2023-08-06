import logging
from typing import Optional

from video_pipeline.video_stream import VideoStream
from video_pipeline.video_stream.video_frame_collector import VideoFrameCollector
import numpy as np
import imageio

try:
    from picamera import PiCamera
except ModuleNotFoundError:
    PiCamera = None
    pass

_logger = logging.getLogger(__name__)


class PiVideoStream(VideoStream):
    """
    A Raspberry PI video stream that can be used to stream video from a PI camera.

    Arguments:
        camera - A PiCamera instance to use to read the video stream.

    Example:
        ```
        with PiVideoStream(PiCamera()) as pi_video_stream:
            frame = pi_video_stream.read():
            # Do something with frame...
        ```
    """
    _camera: PiCamera
    _frame_collector: VideoFrameCollector
    _video_format: str
    _video_format_conversion: str

    def __init__(
        self,
        camera: Optional[PiCamera] = None,
        video_format: str = 'mjpeg'
    ) -> None:
        if camera is None:
            camera = PiCamera()

        super().__init__(
            framerate=camera.framerate
        )

        self._camera = camera
        self._frame_collector = VideoFrameCollector(self._camera.framerate * 2)

        # TODO@nw: Allow different formats. -- We could get a few more frames using: 'bgr', use_video_port=True
        if video_format != 'mjpeg':
            raise ValueError('Only video format "mjpeg" is supported at this time.')
        self._video_format = video_format
        self._video_format_conversion = 'JPEG-PIL'

    def _start_stream(self) -> None:
        # Start recording.
        self._camera.start_recording(
            self._frame_collector,
            format=self._video_format
        )

    def _read_frame(self) -> np.array:
        image_data = self._frame_collector.get_next()  # TODO@nw: This blocks... Might incur a performance hit?
        frame = imageio.imread(
            image_data,
            format=self._video_format_conversion
        )
        return frame

    def _stop_stream(self) -> None:
        # Stop recording.
        try:
            self._camera.stop_recording()
        except Exception as e:
            raise e
        finally:
            self._camera.close()
