import inspect
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from video_pipeline.frame_filter import NoOpFrameFilter
from video_pipeline.frame_filter.color_filter import ColorFilterFrameFilter
from video_pipeline.frame_filter.face_tracker import FaceTrackerFrameFilter
from video_pipeline.frame_filter.find_edges import FindEdgesFrameFilter
from video_pipeline.frame_filter.gray_scale import GrayScaleFrameFilter
from video_pipeline.video_cli.get_frame_filter import _create_color_filter_frame_filter
from video_pipeline.video_cli.get_frame_filter import _create_face_tracker_frame_filter
from video_pipeline.video_cli.get_frame_filter import _create_find_edges_frame_filter
from video_pipeline.video_cli.get_frame_filter import _create_gray_scale_frame_filter
from video_pipeline.video_cli.get_frame_filter import _create_no_op_frame_filter
from video_pipeline.video_cli.get_frame_filter import get_frame_filter
from video_pipeline.video_cli.get_frame_filter import list_frame_filters


def test_list_frame_filters():
    assert list_frame_filters() == [
        'no-op',
        'gray-scale',
        'find-edges',
        'color-filter',
        'face-tracker',
    ]


def test_has_supported_frame_filters():
    # Given a list of supported frame filters
    supported_frame_filters = list_frame_filters()

    for supported_frame_filter in supported_frame_filters:
        # When getting a supported frame filter
        frame_filter_factory = get_frame_filter(supported_frame_filter)

        # Then a frame filter factory is found
        assert callable(frame_filter_factory)

        # Then the factory has the correct number of arguments
        assert len(inspect.getfullargspec(frame_filter_factory)[0]) == 1


def test_has_unsupported_frame_filters():
    # Given a list of unsupported frame filters
    unsupported_frame_filters = [
        'blah',
        'another-blah',
        'lolz',
    ]

    for unsupported_frame_filter in unsupported_frame_filters:
        # When getting an unsupported frame filter
        # Then a frame filter factory is not found
        with pytest.raises(ValueError, match='No FrameFilter found for'):
            get_frame_filter(unsupported_frame_filter)


def test__create_no_op_frame_filter__no_config():
    # When creating a NoOpFrameFilter
    frame_filter = _create_no_op_frame_filter({})

    # Then a NoOpFrameFilter instance was created
    assert isinstance(frame_filter, NoOpFrameFilter)


def test__create_gray_scale_frame_filter__no_config():
    # When creating a gray scale filter
    frame_filter = _create_gray_scale_frame_filter({})

    # Then a GrayScaleFrameFilter instance was created
    assert isinstance(frame_filter, GrayScaleFrameFilter)


def test__create_find_edges_frame_filter__no_config():
    # When creating a find edges filter
    frame_filter = _create_find_edges_frame_filter({})

    # Then a FindEdgesFrameFilter instance was created
    assert isinstance(frame_filter, FindEdgesFrameFilter)


def test__create_color_filter_frame_filter__config():
    # When creating a color filter filter
    with patch.dict('sys.modules', {'cv2': MagicMock()}, clear=True):
        frame_filter = _create_color_filter_frame_filter({
            'color-filter-hsv-lower-limit': '0,0,0',
            'color-filter-hsv-upper-limit': '90,255,255'
        })

        # Then a ColorFilterFrameFilter instance was created
        assert isinstance(frame_filter, ColorFilterFrameFilter)


def test__create_face_tracker_frame_filter__no_config():
    # When creating a face tracker filter
    with patch.dict('sys.modules', {'cv2': MagicMock()}, clear=True):
        frame_filter = _create_face_tracker_frame_filter({})

        # Then a FaceTrackerFrameFilter instance was created
        assert isinstance(frame_filter, FaceTrackerFrameFilter)
