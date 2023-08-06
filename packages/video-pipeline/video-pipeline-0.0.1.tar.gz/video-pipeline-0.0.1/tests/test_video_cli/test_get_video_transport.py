import inspect

import pytest

from video_pipeline.video_cli.get_video_transport import _create_tcp_video_transport
from video_pipeline.video_cli.get_video_transport import get_video_transport
from video_pipeline.video_cli.get_video_transport import list_video_transports
from video_pipeline.video_transport.tcp_video_transport import TcpVideoTransport


def test_list_video_transports():
    assert list_video_transports() == [
        'tcp-server',
        'tcp-client',
        'preview',
    ]


def test_has_supported_video_transports():
    # Given a list of supported video transports
    supported_video_transports = list_video_transports()

    for supported_video_transport in supported_video_transports:
        # When getting a supported video transport
        video_transport_factory = get_video_transport(supported_video_transport)

        # Then a video transport factory is found
        assert callable(video_transport_factory)

        # Then the factory has one argument
        assert len(inspect.getfullargspec(video_transport_factory)[0]) == 1


def test_has_unsupported_video_transports():
    # Given a list of unsupported video transports
    unsupported_video_transports = [
        'blah',
        'another-blah',
        'lolz',
    ]

    for unsupported_video_transport in unsupported_video_transports:
        # When getting an unsupported video transport
        # Then a video transport factory is not found
        with pytest.raises(ValueError, match='No VideoTransport found for'):
            get_video_transport(unsupported_video_transport)


def test__create_video_transport():
    # Given a host and port
    # When creating a video transport
    video_transport = _create_tcp_video_transport(True, {
        'transport-host': '0.0.0.0',
        'transport-port': '8000',
    })

    # Then a tcp video transport was created
    assert isinstance(video_transport, TcpVideoTransport)
