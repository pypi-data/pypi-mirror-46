from unittest.mock import patch
from unittest.mock import MagicMock
import pytest

from video_pipeline.video_processor import VideoProcessor


class MockVideoProcessor(VideoProcessor):
    def _process_frame(self, frame_filter, frame):
        pass

    def _start_processor(self):
        pass

    def _stop_processor(self):
        pass


class TestVideoProcessor:
    @patch.multiple(VideoProcessor, __abstractmethods__=set())
    def test_context_manager(self):
        # Given a base video processor
        video_processor = VideoProcessor()
        with patch.object(video_processor, '_start_processor') as mocked_start_processor, \
                patch.object(video_processor, '_stop_processor') as mocked_stop_processor, \
                patch.object(video_processor, '_process_frame') as mocked_process_frame:

            # When running the video processor
            with video_processor:
                video_processor.process(MagicMock(), MagicMock())
                assert video_processor._is_running

            # Then the appropriate implementation calls were made
            mocked_start_processor.assert_called_once()
            mocked_stop_processor.assert_called_once()
            mocked_process_frame.assert_called_once()

    @patch.multiple(VideoProcessor, __abstractmethods__=set())
    def test_context_manager_raises_exceptions(self):
        # Given a base video processor
        video_processor = VideoProcessor()
        with patch.object(video_processor, '_start_processor'), \
                patch.object(video_processor, '_stop_processor'), \
                patch.object(video_processor, '_process_frame'):

            # When running the video processor and an exception is raised within the context manager
            # Then the exception is not swallowed
            with pytest.raises(ValueError, match='Catch me!'):
                with video_processor:
                    raise ValueError('Catch me!')
