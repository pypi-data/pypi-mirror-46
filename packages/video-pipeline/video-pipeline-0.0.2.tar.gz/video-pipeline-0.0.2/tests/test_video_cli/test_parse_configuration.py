import pytest

from video_pipeline.video_cli.parse_configuration import parse_configuration


def test_parse_configuration__none():
    # Given no configuration variables
    # When parsing the configuration variables
    configuration = parse_configuration([])

    # Then an empty configuration is provided
    assert configuration == {}


def test_parse_configuration__single():
    # Given a single configuration variable
    # When parsing the configuration variable
    configuration = parse_configuration(['my-variable=0'])

    # Then a configuration with the configuration variable is provided
    assert configuration == {
        'my-variable': '0'
    }


def test_parse_configuration__multiple():
    # Given multiple configuration variables
    # When parsing the configuration variables
    configuration = parse_configuration(['my-variable-1=0', 'my-variable-2=abc'])

    # Then a configuration with the configuration variables is provided
    assert configuration == {
        'my-variable-1': '0',
        'my-variable-2': 'abc'
    }


def test_parse_configuration__no_assignment():
    # Given a configuration variable with no assignment
    # When parsing the configuration variables
    # Then a ValueError is raised
    with pytest.raises(ValueError, match='Unable to parse configuration'):
        parse_configuration(['my-variable'])


def test_parse_configuration__multiple_assignments():
    # Given a configuration variable with multiple assignments
    # When parsing the configuration variables
    # Then a ValueError is raised
    with pytest.raises(ValueError, match='Unable to parse configuration'):
        parse_configuration(['my-variable=0=1'])
