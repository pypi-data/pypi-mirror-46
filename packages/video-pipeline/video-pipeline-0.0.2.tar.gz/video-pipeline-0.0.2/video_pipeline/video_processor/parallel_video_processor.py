from collections import deque
from concurrent.futures import Executor
from concurrent.futures import Future
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from queue import Full
from threading import Lock
from typing import List

import numpy as np

from video_pipeline.frame_filter import FrameFilter
from video_pipeline.video_processor import BackPressureError
from video_pipeline.video_processor import BufferOverflowError
from video_pipeline.video_processor import VideoProcessor


class ParallelVideoProcessorExecutorType(Enum):
    PROCESS = 0
    THREAD = 1


def _run_frame_filter(
    frame_filter: FrameFilter,
    frame: np.array,
) -> np.array:
    # Process the image frame.
    return frame_filter.run(frame)


# TODO@nw: Add tests around parallel video processor...
class ParallelVideoProcessor(VideoProcessor):
    """
    A video processor that processes frames in a parallel processing model.

    Arguments:
        frame_buffer_size - The size of the frame buffer of processed frames. (Usually double the video framerate.)
        frame_backlog_size - The max amount of processors to keep running before running into backpressure scenarios.
        executor_pool_size - The amount of processors that can be spun up.
        executor_type - The type of parallel processing executor to use.
    """
    _frame_exceptions: deque
    _active_frame_processors_manager: SyncManager
    _active_frame_processors: List[Future]
    _active_frame_processors_lock: Lock
    _executor: Executor

    def __init__(
        self,
        frame_buffer_size: int = 30,
        frame_backlog_size: int = 15,
        executor_pool_size: int = 15,
        # TODO@nw: Test to make sure video processor is instantiated with correct executor...
        executor_type: ParallelVideoProcessorExecutorType = ParallelVideoProcessorExecutorType.PROCESS
    ) -> None:
        super().__init__(
            frame_buffer_size=frame_buffer_size,
            frame_backlog_size=frame_backlog_size
        )

        self._active_frame_processors_manager = Manager()
        self._active_frame_processors = []
        self._active_frame_processors_lock = self._active_frame_processors_manager.Lock()
        self._frame_exceptions = deque([], maxlen=self._frame_backlog_size)

        # Set executor type.
        if ParallelVideoProcessorExecutorType.PROCESS:
            self._executor = ProcessPoolExecutor(
                max_workers=executor_pool_size
            )
        elif executor_type == ParallelVideoProcessorExecutorType.THREAD:
            self._executor = ThreadPoolExecutor(
                max_workers=executor_pool_size
            )
        else:
            raise ValueError(f'Executor type \'{str(executor_type)}\' not supported.')

    def _start_processor(self) -> None:
        pass

    def _stop_processor(self) -> None:
        # TODO@nw: Add tests around stopping the video processors with active frame processors.
        with self._active_frame_processors_lock:
            for frame_processor in self._active_frame_processors:
                frame_processor.cancel()
            self._executor.shutdown(wait=True)

    def _process_frame(self, frame_filter: FrameFilter, frame: np.array) -> None:
        with self._active_frame_processors_lock:
            if len(self._active_frame_processors) > self._frame_backlog_size:
                raise BackPressureError()

            # TODO@nw: Add tests for backpressure and frame exceptions...
            # TODO@nw: Handle backpressure, output...
            for exception in self._frame_exceptions:
                raise exception

            # Process frame.
            frame_processor = self._executor.submit(
                _run_frame_filter,
                frame_filter,
                frame
            )

            # Append to the queue of active processing frames.
            self._active_frame_processors.append(frame_processor)

            # Handle processed frame.
            frame_processor.add_done_callback(self._on_run_frame_filter_complete)

    def _on_run_frame_filter_complete(self, _just_finished_processor: Future) -> None:
        """Executed when a frame processor has completed processing.

        Supervisor that starts with the oldest frames and checks if they're also done processing.
        Once completed they're removed from the queue and their processed frame appended to the frame buffer.
        """
        # If we're no longer running we need to make sure our frame processors stop doing work.
        if not self._is_running:
            return

        with self._active_frame_processors_lock:
            # Iterate the completed frame processors, in order.
            while len(self._active_frame_processors) > 0:
                # Only append the most recent completed frame.
                most_recent_frame_processor = self._active_frame_processors[0]
                if not most_recent_frame_processor.done():
                    break

                try:
                    # Get the processed frame from the completed processor.
                    processed_frame = most_recent_frame_processor.result()

                    # Add it to our frame buffer.
                    self._frame_buffer.put_nowait(processed_frame)
                    self._fps_counter.count()
                except Full:
                    self._frame_exceptions.append(BufferOverflowError())
                except Exception as e:
                    # TODO@nw: Need to figure out why errors in FrameFilters can crash the executor...
                    self._frame_exceptions.append(e)
                finally:
                    # Remove the most recent frame processors that were completed.
                    self._active_frame_processors.pop()

    def count_processing_frames(self) -> int:
        """Count the active frames being processed.
        """
        # TODO@nw: Like FPS it would be nice to know what the backpressure looks like in real time.
        with self._active_frame_processors_lock:
            return len(self._active_frame_processors)
