import pytest

from video_pipeline.video_stream import VideoStream
from video_pipeline.video_stream import parse_resolution


class MockVideoStream(VideoStream):
    def __init__(self):
        super().__init__(framerate=30)

    def _start_stream(self):
        super()._start_stream()

    def _stop_stream(self):
        super()._stop_stream()

    def _read_frame(self):
        super()._read_frame()


def test_start():
    # Given a VideoStream
    video_stream = MockVideoStream()

    # When a video stream starts
    video_stream.start()

    # Then it should be running
    assert video_stream.is_running()


def test_stop():
    # Given a VideoStream that is already started
    video_stream = MockVideoStream()
    video_stream.start()

    # When a video stream stops
    video_stream.stop()

    # Then it should not be running
    assert not video_stream.is_running()


def test_is_running__on():
    # Given a VideoStream that is running
    video_stream = MockVideoStream()
    video_stream._is_running = True

    # Then the stream should indicate that it is running
    assert video_stream.is_running()


def test_is_running__off():
    # Given a VideoStream that is running
    video_stream = MockVideoStream()
    video_stream._is_running = False

    # Then the stream should indicate that it is not running
    assert not video_stream.is_running()


def test_double_start():
    # Given a video stream that is already started
    with MockVideoStream() as video_stream:
        # When it starts again
        # Then it raises a ValueError
        with pytest.raises(ValueError):
            video_stream.start()


def test_double_stop():
    # Given a video stream that is already stopped
    with pytest.raises(ValueError):
        # When it stops again
        # Then it raises a ValueError
        with MockVideoStream() as video_stream:
            video_stream.stop()


def test_context_manager_raises_exceptions():
    # Given a video stream that is already started
    video_stream = MockVideoStream()

    # When an exception is raised within the context manager
    # Then the exception is not swallowed
    with pytest.raises(ValueError, match='Catch me!'):
        with video_stream:
            raise ValueError('Catch me!')


def test_parse_resolution__valid():
    # When parsing a valid resolution
    resolution = parse_resolution('640x320')

    # Then we get back the right resolution format
    assert resolution == (640, 320)


def test_parse_resolution__invalid_height():
    # When parsing an invalid height
    # Then we get a ValueError
    with pytest.raises(ValueError, match='Unable to parse provided resolution'):
        parse_resolution('640xrst')


def test_parse_resolution__invalid_width():
    # When parsing an invalid width
    # Then we get a ValueError
    with pytest.raises(ValueError, match='Unable to parse provided resolution'):
        parse_resolution('tssdfx320')


def test_parse_resolution__no_height_or_width():
    # When parsing a resolution with no height or width
    # Then we get a ValueError
    with pytest.raises(ValueError, match='Unable to parse provided resolution'):
        parse_resolution('tssdf')
