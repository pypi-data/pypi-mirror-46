import functools
from typing import Callable
from typing import Dict
from typing import List

from video_pipeline.video_stream import parse_resolution
from video_pipeline.video_transport import VideoTransport
from video_pipeline.video_transport.file_video_transport import FileVideoTransport
from video_pipeline.video_transport.tcp_video_transport import TcpVideoTransport
from video_pipeline.video_transport.visvis_video_transport import VisVisVideoTransport


def _create_tcp_video_transport(
    is_server: bool,
    config: Dict[str, str]
) -> VideoTransport:
    # Get appropriate configuration.
    socket_host = config['transport-host']
    socket_port = int(config['transport-port'])

    # Construct the transport component.
    return TcpVideoTransport(
        socket_host=socket_host,
        socket_port=socket_port,
        is_server=True
    )


def _create_preview_video_transport(
    config: Dict[str, str]
) -> VideoTransport:
    # Get appropriate configuration.
    resolution = parse_resolution(config['source-resolution'])

    # Construct the transport component.
    return VisVisVideoTransport(
        starting_window_resolution=resolution
    )


def _create_file_video_transport(
    config: Dict[str, str]
) -> VideoTransport:
    # Get appropriate configuration.
    file_path = config['transport-file']

    return FileVideoTransport(
        file_path=file_path
    )


_available_video_transports = {
    'tcp-server': functools.partial(_create_tcp_video_transport, True),
    'tcp-client': functools.partial(_create_tcp_video_transport, False),
    'preview': functools.partial(_create_preview_video_transport),
    'file': functools.partial(_create_file_video_transport),
}


def get_video_transport(transport: str) -> Callable[[Dict[str, str]], VideoTransport]:
    # Do we have an implementation for this transport?
    if transport not in _available_video_transports:
        raise ValueError(f'No VideoTransport found for "{transport}".')

    # Found an available implementation.
    return _available_video_transports[transport]


def list_video_transports() -> List[str]:
    return list(_available_video_transports.keys())
