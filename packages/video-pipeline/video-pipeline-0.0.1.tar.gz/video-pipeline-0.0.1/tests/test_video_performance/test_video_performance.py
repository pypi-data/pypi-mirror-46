from video_pipeline.video_performance import FpsCounter
from unittest.mock import patch
from unittest.mock import MagicMock


def test_thirty_frames_per_second():
    # Given a desired framerate of 30fps
    framerate = 30

    # And a FpsCounter with half the framerate for sample size
    fps_counter = FpsCounter(framerate // 2)

    # And the OS can provide us an accurate time
    mocked_perf_counter = MagicMock()

    def perf_counter_side_effect():
        return mocked_perf_counter.call_count * framerate
    mocked_perf_counter.side_effect = perf_counter_side_effect

    # When counting frames up to the sample size
    with patch('time.perf_counter', new=mocked_perf_counter):
        for _ in range(framerate // 2 - 1):
            fps_counter.count()

        # Then the counter does not calculate fps
        mocked_perf_counter.assert_not_called()

        # When counting surpasses the sample size
        fps_counter.count()

        # Then the counter calculates fps
        mocked_perf_counter.assert_called_once()


def test_sixty_frames_per_second():
    # Given a desired framerate of 60fps
    framerate = 60

    # And a FpsCounter with half the framerate for sample size
    fps_counter = FpsCounter(framerate // 2)

    # And the OS can provide us an accurate time
    mocked_perf_counter = MagicMock()

    def perf_counter_side_effect():
        return mocked_perf_counter.call_count * framerate
    mocked_perf_counter.side_effect = perf_counter_side_effect

    # When counting frames up to the sample size
    with patch('time.perf_counter', new=mocked_perf_counter):
        for _ in range(framerate // 2 - 1):
            fps_counter.count()

        # Then the counter does not calculate fps
        mocked_perf_counter.assert_not_called()

        # When counting surpasses the sample size
        fps_counter.count()

        # Then the counter calculates fps
        mocked_perf_counter.assert_called_once()
