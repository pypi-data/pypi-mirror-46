from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import PropertyMock
from unittest.mock import call

from video_pipeline.video_cli.get_metrics_handler import MetricsHandler
from video_pipeline.video_cli.get_metrics_handler import PipeMetricsHandler
from video_pipeline.video_cli.get_metrics_handler import SpinnerMetricsHandler
from video_pipeline.video_cli.get_metrics_handler import Metrics


class TestMetricsHandler:
    @patch.multiple(MetricsHandler, __abstractmethods__=set())
    def test_context_manager(self):
        # Given a base metrics handler
        metrics_handler = MetricsHandler()
        with patch.object(metrics_handler, '_start') as mocked_start, \
                patch.object(metrics_handler, '_stop') as mocked_stop, \
                patch.object(metrics_handler, '_perform') as mocked_perform:

            # When running the metrics handler as a context manager
            with metrics_handler:
                metrics_handler.perform(None, None, None)

            # Then the appropriate implementation calls were made
            mocked_start.assert_called_once()
            mocked_stop.assert_called_once()
            mocked_perform.assert_called_once()


class TestPipeMetricsHandler:
    @patch('video_pipeline.video_cli.get_metrics_handler._get_metrics')
    @patch('video_pipeline.video_cli.get_metrics_handler._logger')
    def test_perform(self, mocked_logger, mocked_get_metrics):
        # Given some metric data
        # And a viable output
        mocked_get_metrics.return_value = Metrics(
            stream_fps=30,
            processor_fps=42
        )

        # And a pipe metrics handler
        with PipeMetricsHandler() as metrics_handler:
            # When handling video pipeline metrics
            metrics_handler.perform(None, None, None)

        # Then the metrics were properly outputted
        mocked_logger.info.assert_has_calls([
            call('Stream FPS,Processor FPS'),
            call('30,42')
        ])


class TestSpinnerMetricsHandler:
    @patch('video_pipeline.video_cli.get_metrics_handler._get_metrics')
    @patch('video_pipeline.video_cli.get_metrics_handler.Halo')
    def test_perform(self, MockedHalo, mocked_get_metrics):
        # Given some metric data
        mocked_get_metrics.return_value = Metrics(
            stream_fps=30,
            processor_fps=42
        )

        # And an active spinner
        mocked_spinner = MagicMock()
        mocked_spinner_text = PropertyMock()
        type(mocked_spinner).text = mocked_spinner_text
        MockedHalo.return_value = mocked_spinner

        # And a spinner metrics handler
        with SpinnerMetricsHandler() as metrics_handler:
            # When handling video pipeline metrics
            metrics_handler.perform(None, None, None)

        # Then the metrics were properly outputted
        mocked_spinner.start.assert_called_once()
        mocked_spinner.stop.assert_called_once()
        mocked_spinner_text.assert_called_once_with(
            f'[ (VideoStream 30fps) --> (VideoProcessor 42fps) ]'
        )
