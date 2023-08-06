from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from video_pipeline.video_stream.pi_video_stream import PiVideoStream


@pytest.yield_fixture
def create_pi_video_stream():
    """Since the module `picamera` cannot be installed on 'non-compliant' devices
    we need to mock out it's import directly instead of using `patch`.

    Returns:
        PiVideoStream - With mocked out picamera.
    """
    def create_pi_video_stream_imp():
        with patch('video_pipeline.video_stream.pi_video_stream.PiCamera') as MockedPiCamera:
            # Instantiate a mocked pi video stream with a default framerate.
            mocked_camera = MockedPiCamera()
            mocked_camera.framerate = 30
            return PiVideoStream()

    yield create_pi_video_stream_imp


def test_double_start(create_pi_video_stream):
    # Given a PI video stream that is already started
    with create_pi_video_stream() as pi_video_stream:
        # When it starts again
        # Then it raises a ValueError
        with pytest.raises(ValueError):
            pi_video_stream.start()


def test_double_stop(create_pi_video_stream):
    # Given a PI video stream that is already stopped
    with create_pi_video_stream() as pi_video_stream:
        pass

    with pytest.raises(ValueError):
        # When it stops again
        # Then it raises a ValueError
        with pi_video_stream:
            pi_video_stream.stop()


def test_camera_start(create_pi_video_stream):
    # Given a PI video stream
    # When it starts
    with create_pi_video_stream() as pi_video_stream:
        picamera = pi_video_stream._camera

    # Then the picamera starts recording
    picamera.start_recording.assert_called_once()


def test_camera_stop(create_pi_video_stream):
    # Given a PI video stream
    # When it stops
    with create_pi_video_stream() as pi_video_stream:
        picamera = pi_video_stream._camera

    # Then the picamera stops recording
    picamera.stop_recording.assert_called_once()


def test_read(create_pi_video_stream):
    # Given a PI video stream
    mocked_frame_collector = MagicMock()
    mocked_fps_counter = MagicMock()

    with patch(
        'video_pipeline.video_stream.pi_video_stream.VideoFrameCollector',
        new=MagicMock(return_value=mocked_frame_collector)
    ), \
        patch(
        'video_pipeline.video_stream.FpsCounter',
        new=MagicMock(return_value=mocked_fps_counter)
    ), \
        patch(
        'video_pipeline.video_stream.pi_video_stream.imageio.imread',
    ) as mocked_frame_reader:
        with create_pi_video_stream() as pi_video_stream:
            # When reading a frame
            pi_video_stream.read()

            # Then the frame collector was called
            mocked_frame_collector.get_next.assert_called_once()

            # Then the fps counter was called
            mocked_fps_counter.count.assert_called_once()

            # Then the frame reader was called
            mocked_frame_reader.assert_called_once()
