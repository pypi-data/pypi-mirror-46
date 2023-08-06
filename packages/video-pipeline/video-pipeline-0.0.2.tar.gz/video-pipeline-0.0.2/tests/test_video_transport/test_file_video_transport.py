from unittest.mock import MagicMock
from unittest.mock import patch

from video_pipeline.video_transport.file_video_transport import FileVideoTransport


def test_start():
    # Given a FileVideoTransport with a file to write to
    with patch(
        'video_pipeline.video_transport.file_video_transport.open'
    ) as mocked_open:
        video_transport = FileVideoTransport('output.mp4')

        # When the transport starts
        video_transport.start()

        # Then it should open the appropriate file
        mocked_open.assert_called_once_with('output.mp4', 'wb')


def test_stop():
    # Given a FileVideoTransport that is already running with an active file
    video_transport = FileVideoTransport('output.mp4')
    video_transport._is_running = True
    mocked_file = video_transport._file = MagicMock()

    # When the transport stops
    video_transport.stop()

    # Then it should close the appropriate file
    mocked_file.close.assert_called_once()
