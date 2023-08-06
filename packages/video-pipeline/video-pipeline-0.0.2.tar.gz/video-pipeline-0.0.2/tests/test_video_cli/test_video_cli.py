from unittest.mock import patch

from video_pipeline.video_cli.__main__ import VideoCli


@patch('video_pipeline.video_cli.__main__.run_pipeline')
@patch('video_pipeline.video_cli.__main__.get_video_stream')
@patch('video_pipeline.video_cli.__main__.get_frame_filter')
@patch('video_pipeline.video_cli.__main__.get_video_processor')
@patch('video_pipeline.video_cli.__main__.get_video_transport')
def test_command__start(
    mocked_get_video_transport,
    mocked_get_video_processor,
    mocked_get_frame_filter,
    mocked_get_video_stream,
    mocked_run_pipeline
):
    # Given a video-pipeline CLI
    # And video pipeline component factories
    video_cli = VideoCli()

    # When invoking the 'start' command
    video_cli.run(['start'])

    # Then the command is executed, constructing all the necessary pipeline components
    mocked_get_video_stream.assert_called_once()
    mocked_get_frame_filter.assert_called_once()
    mocked_get_video_processor.assert_called_once()
    mocked_get_video_transport.assert_called_once()

    # Then the pipeline is executed
    mocked_run_pipeline.assert_called_once()


@patch('video_pipeline.video_cli.__main__.list_video_streams')
def test_command__list_sources(mocked_list_video_streams):
    # Given a video-pipeline CLI
    video_cli = VideoCli()

    # When invoking the 'list-sources' command
    video_cli.run(['list-sources'])

    # Then the command is executed
    mocked_list_video_streams.assert_called_once()


@patch('video_pipeline.video_cli.__main__.list_frame_filters')
def test_command__list_filters(mocked_list_frame_filters):
    # Given a video-pipeline CLI
    video_cli = VideoCli()

    # When invoking the 'list-filters' command
    video_cli.run(['list-filters'])

    # Then the command is executed
    mocked_list_frame_filters.assert_called_once()


@patch('video_pipeline.video_cli.__main__.list_video_processors')
def test_command__list_processors(mocked_list_video_processors):
    # Given a video-pipeline CLI
    video_cli = VideoCli()

    # When invoking the 'list-processors' command
    video_cli.run(['list-processors'])

    # Then the command is executed
    mocked_list_video_processors.assert_called_once()


@patch('video_pipeline.video_cli.__main__.list_video_transports')
def test_command__list_transports(mocked_list_video_transports):
    # Given a video-pipeline CLI
    video_cli = VideoCli()

    # When invoking the 'list-transports' command
    video_cli.run(['list-transports'])

    # Then the command is executed
    mocked_list_video_transports.assert_called_once()
