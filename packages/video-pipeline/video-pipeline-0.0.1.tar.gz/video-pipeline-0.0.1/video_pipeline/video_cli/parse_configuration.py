from multiprocessing import cpu_count
from typing import Dict
from typing import List
from typing import Tuple

_default_configuration: Dict[str, str] = {
    'source-framerate': '30',
    'source-resolution': '960x640',
    'transport-host': '0.0.0.0',
    'transport-port': '8000',
    'processor-processes': f'{cpu_count()}',
    'processor-buffer-multiplier': '1',
    'processor-executor-type': 'PROCESS',
}


def parse_configuration(
    configuration_variables: List[str],
    delimiter: str = '='
) -> Dict[str, str]:
    """Parse configuration variables.

    Example:
        >>> parse_configuration(['source-resolution=960x640', 'source-framerate=90'])
        {
            'source-resolution': '960x640',
            'source-framerate': '90',
        }
    """
    def _parse_configuration(formatted_configuration: str) -> Tuple[str, str]:
        split_configuration: List[str] = formatted_configuration.split(delimiter)
        if len(split_configuration) != 2:
            raise ValueError(f'Unable to parse configuration \'{formatted_configuration}\'.')
        return (split_configuration[0], split_configuration[1])

    parsed_configurations = (
        _parse_configuration(configuration_variable)
        for configuration_variable in configuration_variables
    )

    return {key: value for (key, value) in parsed_configurations}


def get_default_configuration() -> Dict[str, str]:
    return _default_configuration
