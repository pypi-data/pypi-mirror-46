import pytest
from video_pipeline.video_transport import VideoTransport


class MockVideoTransport(VideoTransport):
    def __init__(self):
        super().__init__()

    def _start_transport(self):
        super()._start_transport()

    def _stop_transport(self):
        super()._stop_transport()

    def _transport_frame(self):
        super()._transport_frame()


def test_start():
    # Given a VideoTransport
    video_transport = MockVideoTransport()

    # When a video transport starts
    video_transport.start()

    # Then it should be running
    assert video_transport.is_running()


def test_stop():
    # Given a VideoTransport that is already started
    video_transport = MockVideoTransport()
    video_transport.start()

    # When a video transport stops
    video_transport.stop()

    # Then it should not be running
    assert not video_transport.is_running()


def test_is_running__on():
    # Given a VideoTransport that is running
    video_transport = MockVideoTransport()
    video_transport._is_running = True

    # Then the transport should indicate that it is running
    assert video_transport.is_running()


def test_is_running__off():
    # Given a VideoTransport that is running
    video_transport = MockVideoTransport()
    video_transport._is_running = False

    # Then the transport should indicate that it is not running
    assert not video_transport.is_running()


def test_double_start():
    # Given a video transport that is already started
    with MockVideoTransport() as video_transport:
        # When it starts again
        # Then it raises a ValueError
        with pytest.raises(ValueError):
            video_transport.start()


def test_double_stop():
    # Given a video transport that is already stopped
    with pytest.raises(ValueError):
        # When it stops again
        # Then it raises a ValueError
        with MockVideoTransport() as video_transport:
            video_transport.stop()


def test_context_manager_raises_exceptions():
    # Given a video transport that is already started
    video_transport = MockVideoTransport()

    # When an exception is raised within the context manager
    # Then the exception is not swallowed
    with pytest.raises(ValueError, match='Catch me!'):
        with video_transport:
            raise ValueError('Catch me!')
