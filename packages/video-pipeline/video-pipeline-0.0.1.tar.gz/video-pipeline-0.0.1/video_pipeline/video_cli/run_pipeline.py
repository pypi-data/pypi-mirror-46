import logging
import time

from video_pipeline.frame_filter import FrameFilter
from video_pipeline.video_cli.get_metrics_handler import MetricsHandler
from video_pipeline.video_processor import BackPressureError
from video_pipeline.video_processor import BufferEmptyError
from video_pipeline.video_processor import BufferOverflowError
from video_pipeline.video_processor import VideoProcessor
from video_pipeline.video_stream import VideoStream
from video_pipeline.video_transport import VideoTransport

_logger = logging.getLogger(__name__)


def run_pipeline(
    video_stream: VideoStream,
    frame_filter: FrameFilter,
    video_processor: VideoProcessor,
    video_transport: VideoTransport,
    metrics_handler: MetricsHandler,
) -> None:
    # Start up the pipeline.
    video_stream.start()
    video_processor.start()
    video_transport.start()
    metrics_handler.start()
    is_running = True

    try:
        previous_time = time.perf_counter()

        # Continuesly read frames.
        while is_running:
            # Calculate real-time metrics.
            now_time = time.perf_counter()
            elapsed_time = now_time - previous_time
            if elapsed_time >= 1.20:
                metrics_handler.perform(video_stream, video_processor, video_transport)
                previous_time = now_time

            # Read frame.
            frame = video_stream.read()

            # Process frame.
            # TODO@nw: Might be really nice to use generators here to help manage backpressure instead of exceptions.
            video_processor.process(frame_filter, frame)
            processed_frame = video_processor.read()

            # Transport processed frame.
            video_transport.transport(processed_frame)
    except BackPressureError:
        pass
    except BufferEmptyError:
        pass
    except BufferOverflowError:
        pass
    except Exception as e:
        _logger.exception(e)
        _logger.info('Shuting down...')
    finally:
        is_running = False
        video_transport.stop()
        video_processor.stop()
        video_stream.stop()
        metrics_handler.stop()
