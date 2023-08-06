from typing import Callable
from typing import Dict
from typing import List

from video_pipeline.video_stream import VideoStream
from video_pipeline.video_stream import parse_resolution
from video_pipeline.video_stream.os_video_stream import OsVideoStream
from video_pipeline.video_stream.pi_video_stream import PiVideoStream


def _create_pi_video_stream(config: Dict[str, str]) -> VideoStream:
    # Get appropriate configuration.
    resolution = parse_resolution(config['source-resolution'])
    framerate = int(config['source-framerate'])

    # Construct the stream component.
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = framerate

    return PiVideoStream(camera)


# TODO@nw: Add os video stream support.
# TODO@nw:  add tests
def _create_os_video_stream(config: Dict[str, str]) -> VideoStream:
    # Get appropriate configuration.
    resolution = parse_resolution(config['source-resolution'])
    framerate = int(config['source-framerate'])

    # Construct the stream component.
    return OsVideoStream(
        framerate=framerate,
        resolution=resolution
    )


_available_video_streams = {
    # TODO@nw: It's very possible that we could merge these...
    'pi': _create_pi_video_stream,
    'os': _create_os_video_stream
}


def get_video_stream(source: str) -> Callable[[Dict[str, str]], VideoStream]:
    # Do we have an implementation for this source?
    if source not in _available_video_streams:
        raise ValueError(f'No VideoStream found for "{source}".')

    # Found an available implementation.
    return _available_video_streams[source]


def list_video_streams() -> List[str]:
    return list(_available_video_streams.keys())
