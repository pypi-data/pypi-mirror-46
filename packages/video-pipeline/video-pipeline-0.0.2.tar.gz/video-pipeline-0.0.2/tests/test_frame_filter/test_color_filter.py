import pytest

from video_pipeline.frame_filter.color_filter import HsvErrorCode
from video_pipeline.frame_filter.color_filter import HsvParseError
from video_pipeline.frame_filter.color_filter import parse_hsv


def test_parse_hsv():
    # Given a valid hsv
    # When parsing the hsv
    hsv = parse_hsv('0,150,100')

    # Then a valid hsv was parsed
    assert hsv == (0.0, 150, 100)


def test_parse_hsv__spaces():
    # Given a valid hsv with spaces
    # When parsing the hsv
    hsv = parse_hsv('0 , 150 , 100 ')

    # Then a valid hsv was parsed
    assert hsv == (0.0, 150, 100)


def test_parse_hsv__invalid__hue_nan():
    # Given an invalid hsv where the hue is NaN
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('a,150,100')

    assert error.value.parse_error == HsvErrorCode.HUE


def test_parse_hsv__valid_hue_float():
    # Given a valid hsv where the hue is a float
    # When parsing the hsv
    hsv = parse_hsv('0.4,150,100')

    # Then a valid hsv was parsed
    assert hsv == (0.4, 150, 100)


def test_parse_hsv__invalid_hue__bellow_0():
    # Given an invalid hsv where the hue is bellow 0 degrees
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('-1,150,100')

    assert error.value.parse_error == HsvErrorCode.HUE


def test_parse_hsv__invalid_hue__above_360():
    # Given an invalid hsv where the hue is above 360 degrees
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('370,150,100')

    assert error.value.parse_error == HsvErrorCode.HUE


def test_parse_hsv__invalid__saturation_nan():
    # Given an invalid hsv where the saturation is NaN
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,x,100')

    assert error.value.parse_error == HsvErrorCode.SATURATION


def test_parse_hsv__invalid__saturation_float():
    # Given an invalid hsv where the saturation is a float
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,150.5,100')

    assert error.value.parse_error == HsvErrorCode.SATURATION


def test_parse_hsv__invalid_saturation__bellow_0():
    # Given an invalid hsv where the saturation is bellow uint8 0
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,-1,100')

    assert error.value.parse_error == HsvErrorCode.SATURATION


def test_parse_hsv__invalid_saturation__above_255():
    # Given an invalid hsv where the saturation is above uint8 255
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,350,100')

    assert error.value.parse_error == HsvErrorCode.SATURATION


def test_parse_hsv__invalid__value_nan():
    # Given an invalid hsv where the value is NaN
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,150,y')

    assert error.value.parse_error == HsvErrorCode.VALUE


def test_parse_hsv__invalid__value_float():
    # Given an invalid hsv where the value is a float
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,150,100.3')

    assert error.value.parse_error == HsvErrorCode.VALUE


def test_parse_hsv__invalid_value__bellow_0():
    # Given an invalid hsv where the value is bellow uint8 0
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,150,-1')

    assert error.value.parse_error == HsvErrorCode.VALUE


def test_parse_hsv__invalid_value__above_255():
    # Given an invalid hsv where the value is above uint8 255
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,150,300')

    assert error.value.parse_error == HsvErrorCode.VALUE


def test_parse_hsv__invalid__missing_values():
    # Given an invalid hsv where some values are missing
    # When parsing the hsv
    # Then a parsing error occurs
    with pytest.raises(HsvParseError) as error:
        parse_hsv('0,150')

    assert error.value.parse_error == HsvErrorCode.MISSING_VALUES
