from unittest.mock import patch
from unittest.mock import MagicMock
import sys

import pytest
import inspect

from video_pipeline.video_stream.pi_video_stream import PiVideoStream
from video_pipeline.video_cli.get_video_stream import _create_pi_video_stream
from video_pipeline.video_cli.get_video_stream import get_video_stream
from video_pipeline.video_cli.get_video_stream import list_video_streams


def test_list_video_processors():
    assert list_video_streams() == [
        'pi',
        'os',
    ]


def test_has_supported_video_streams():
    # Given a list of supported video streams
    supported_video_streams = list_video_streams()

    for supported_video_stream in supported_video_streams:
        # When getting a supported video stream
        video_stream_factory = get_video_stream(supported_video_stream)

        # Then a video stream factory is found
        assert callable(video_stream_factory)

        # Then the factory one argument
        assert len(inspect.getfullargspec(video_stream_factory)[0]) == 1


def test_has_unsupported_video_streams():
    # Given a list of unsupported video streams
    unsupported_video_streams = [
        'blah',
        'another-blah',
        'lolz',
    ]

    for unsupported_video_stream in unsupported_video_streams:
        # When getting an unsupported video stream
        # Then a video stream factory is not found
        with pytest.raises(ValueError, match='No VideoStream found for'):
            get_video_stream(unsupported_video_stream)


def test__create_pi_video_stream():
    # Given a resolution of 320x240 and framerate of 30
    # When creating a pi video stream
    sys.modules['picamera'] = MagicMock()
    with patch('picamera.PiCamera') as MockedPiCamera:
        video_stream = _create_pi_video_stream({
            'source-resolution': '320x240',
            'source-framerate': '30'
        })

        # Then a pi video stream is created
        assert isinstance(video_stream, PiVideoStream)

        # Then picamera was created
        MockedPiCamera.assert_called_once()
