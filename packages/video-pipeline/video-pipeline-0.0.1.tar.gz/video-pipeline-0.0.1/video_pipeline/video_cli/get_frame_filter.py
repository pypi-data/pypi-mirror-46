from typing import Callable
from typing import Dict
from typing import List

from video_pipeline.frame_filter import FrameFilter
from video_pipeline.frame_filter import NoOpFrameFilter
from video_pipeline.frame_filter.color_filter import ColorFilterFrameFilter
from video_pipeline.frame_filter.find_edges import FindEdgesFrameFilter
from video_pipeline.frame_filter.gray_scale import GrayScaleFrameFilter


def _create_no_op_frame_filter(
    config: Dict[str, str]
) -> FrameFilter:
    return NoOpFrameFilter()


def _create_gray_scale_frame_filter(
    config: Dict[str, str]
) -> FrameFilter:
    return GrayScaleFrameFilter()


def _create_find_edges_frame_filter(
    config: Dict[str, str]
) -> FrameFilter:
    return FindEdgesFrameFilter()


def _create_color_filter_frame_filter(
    config: Dict[str, str]
) -> FrameFilter:
    return ColorFilterFrameFilter()


_available_frame_filters = {
    'no-op': _create_no_op_frame_filter,
    'gray-scale': _create_gray_scale_frame_filter,
    'find-edges': _create_find_edges_frame_filter,
    'color-filter': _create_color_filter_frame_filter,
}


def get_frame_filter(filter: str) -> Callable[[Dict[str, str]], FrameFilter]:
    # Do we have an implementation for this filter?
    if filter not in _available_frame_filters:
        raise ValueError(f'No FrameFilter found for "{filter}".')

    # Found an available implementation.
    return _available_frame_filters[filter]


def list_frame_filters() -> List[str]:
    return list(_available_frame_filters.keys())
