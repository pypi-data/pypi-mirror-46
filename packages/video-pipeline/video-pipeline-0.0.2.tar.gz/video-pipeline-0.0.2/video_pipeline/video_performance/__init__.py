import time


class FpsCounter:
    """Samples frames per second (FPS) when we've counted more than our sample size.

    Arguments:
        sample_size - How many frames should we sample before recalculating FPS.
    """
    _sample_size: int
    _frame_count: int
    _current_fps: int
    _previous_time: float

    def __init__(self, sample_size: int) -> None:
        self._sample_size = sample_size
        self._frame_count = 0
        self._current_fps = 0
        self._previous_time = 0

    def fps(self) -> int:
        return self._current_fps

    def count(self) -> None:
        # TODO@nw: Add FPS test.
        self._frame_count += 1
        if self._frame_count >= self._sample_size:
            now_time = time.perf_counter()
            self._current_fps = round(self._frame_count /
                                      (now_time - self._previous_time))
            self._previous_time = now_time
            self.reset()

    def reset(self) -> None:
        self._frame_count = 0

    # TODO@nw: Add test...
    def clear(self) -> None:
        self.reset()
        self._current_fps = 0
