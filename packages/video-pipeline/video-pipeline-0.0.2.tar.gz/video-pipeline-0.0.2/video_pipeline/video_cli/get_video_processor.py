import functools
from typing import Callable
from typing import Dict
from typing import List

from video_pipeline.video_processor import VideoProcessor
from video_pipeline.video_processor.parallel_video_processor import ParallelVideoProcessor
from video_pipeline.video_processor.parallel_video_processor import ParallelVideoProcessorExecutorType
from video_pipeline.video_processor.serial_video_processor import SerialVideoProcessor


def _create_parallel_video_processor(config: Dict[str, str]) -> VideoProcessor:
    # Get appropriate configuration.
    framerate = int(config['source-framerate'])
    processes = int(config['processor-processes'])
    buffer_multiplier = int(config['processor-buffer-multiplier'])
    try:
        executor_type = ParallelVideoProcessorExecutorType[config['processor-executor-type']]
    except KeyError:
        raise ValueError('Unable to parse \'processor-executor-type\'. Check the available executor types.')

    # Construct the processor component.
    return ParallelVideoProcessor(
        frame_buffer_size=framerate * buffer_multiplier,
        frame_backlog_size=framerate * buffer_multiplier,
        executor_pool_size=processes,
        executor_type=executor_type
    )


def _create_serial_video_processor(config: Dict[str, str]) -> VideoProcessor:
    # Get appropriate configuration.
    framerate = int(config['source-framerate'])
    buffer_multiplier = int(config['processor-buffer-multiplier'])

    # Construct the processor component.
    return SerialVideoProcessor(
        frame_buffer_size=framerate * buffer_multiplier,
        frame_backlog_size=framerate * buffer_multiplier
    )


_available_video_processors = {
    'parallel': functools.partial(_create_parallel_video_processor),
    'serial': functools.partial(_create_serial_video_processor),
}


def get_video_processor(processor_type: str) -> Callable[[Dict[str, str]], VideoProcessor]:
    # Do we have an implementation for this processor type?
    if processor_type not in _available_video_processors:
        raise ValueError(f'No VideoProcessor found for "{processor_type}".')

    # Found an available implementation.
    return _available_video_processors[processor_type]


def list_video_processors() -> List[str]:
    return list(_available_video_processors.keys())
