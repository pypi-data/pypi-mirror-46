import inspect

import pytest

from video_pipeline.video_cli.get_video_processor import get_video_processor
from video_pipeline.video_cli.get_video_processor import list_video_processors
from video_pipeline.video_processor.parallel_video_processor import ParallelVideoProcessor
from video_pipeline.video_processor.serial_video_processor import SerialVideoProcessor


def test_list_frame_filters():
    assert list_video_processors() == [
        'parallel',
        'serial'
    ]


def test_has_supported_video_processors():
    # Given a list of supported video processors
    supported_video_processors = list_video_processors()

    for supported_video_processor in supported_video_processors:
        # When getting a supported video processor
        video_processor_factory = get_video_processor(supported_video_processor)

        # Then a video processor factory is found
        assert callable(video_processor_factory)

        # Then the factory has the correct number of arguments
        assert len(inspect.getfullargspec(video_processor_factory)[0]) == 1


def test_has_unsupported_video_processors():
    # Given a list of unsupported video processors
    unsupported_video_processors = [
        'blah',
        'another-blah',
        'lolz',
    ]

    for unsupported_video_processor in unsupported_video_processors:
        # When getting an unsupported video processor
        # Then a video processor factory is not found
        with pytest.raises(ValueError, match='No VideoProcessor found for'):
            get_video_processor(unsupported_video_processor)


def test_get_video_processor__parallel__default_config():
    # When getting a 'parallel' video processor
    video_processor = get_video_processor('parallel')({
        'source-framerate': '30',
        'processor-buffer-multiplier': '5',
        'processor-processes': '2',
        'processor-executor-type': 'PROCESS'
    })

    # Then it is a 'parallel' video processor
    assert isinstance(video_processor, ParallelVideoProcessor)


def test_get_video_processor__serial__default_config():
    # When getting a 'serial' video processor
    video_processor = get_video_processor('serial')({
        'source-framerate': '30',
        'processor-buffer-multiplier': '5'
    })

    # Then it is a 'serial' video processor
    assert isinstance(video_processor, SerialVideoProcessor)
