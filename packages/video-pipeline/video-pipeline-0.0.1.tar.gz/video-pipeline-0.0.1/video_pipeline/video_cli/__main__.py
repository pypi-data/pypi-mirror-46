import logging
import os
import sys
from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction
from typing import Dict
from typing import List
from typing import Optional

from video_pipeline import __version__
from video_pipeline.video_cli.get_frame_filter import get_frame_filter
from video_pipeline.video_cli.get_frame_filter import list_frame_filters
from video_pipeline.video_cli.get_metrics_handler import get_metrics_handler
from video_pipeline.video_cli.get_video_processor import get_video_processor
from video_pipeline.video_cli.get_video_processor import list_video_processors
from video_pipeline.video_cli.get_video_stream import get_video_stream
from video_pipeline.video_cli.get_video_stream import list_video_streams
from video_pipeline.video_cli.get_video_transport import get_video_transport
from video_pipeline.video_cli.get_video_transport import list_video_transports
from video_pipeline.video_cli.parse_configuration import get_default_configuration
from video_pipeline.video_cli.parse_configuration import parse_configuration
from video_pipeline.video_cli.run_pipeline import run_pipeline

_logger = logging.getLogger('video-pipeline')


class VideoCli:
    def __init__(self) -> None:
        self._parser = self._create_parser()

    def _create_start_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        start_parser = subparsers.add_parser(
            'start',
            help='Start running a video-pipeline.'
        )

        start_parser.add_argument(
            '--source',
            default='webcam',
            type=str,
            help='Where to pull a video stream.'
        )
        start_parser.add_argument(
            '--filter',
            default='noop',
            type=str,
            help='How to transform the video stream.'
        )
        start_parser.add_argument(
            '--processor',
            default='parallel',
            type=str,
            help='Which processing mechanism to use.'
        )
        start_parser.add_argument(
            '--transport',
            default='tcp-server',
            type=str,
            help='Where to send the video stream after filtering.'
        )
        start_parser.add_argument(
            'vars',
            nargs='*',
            help='Additional configuration for video pipeline modules.'
        )

        return start_parser

    def _create_list_sources_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        list_sources_parser = subparsers.add_parser(
            'list-sources',
            help='Lists available sources to use.'
        )

        return list_sources_parser

    def _create_list_filters_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        list_filters_parser = subparsers.add_parser(
            'list-filters',
            help='Lists available filters to use.'
        )

        return list_filters_parser

    def _create_list_processors_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        list_processors_parser = subparsers.add_parser(
            'list-processors',
            help='Lists available processors to use.'
        )

        return list_processors_parser

    def _create_list_transports_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        list_transports_parser = subparsers.add_parser(
            'list-transports',
            help='Lists available transports to use.'
        )

        return list_transports_parser

    def _create_parser(self) -> ArgumentParser:
        # create top level argument parser.
        parser = ArgumentParser(
            description='Frame by frame image manipulation of a video stream in near real-time.',
            prog='video-pipeline'
        )
        parser.add_argument(
            '--version',
            action='version',
            version=f'video-pipeline {__version__}'
        )
        parser.add_argument(
            '--no-logo',
            action='store_true',
            help='Hide logo when running.'
        )
        parser.add_argument('-v', '--verbose', action='count', default=0)

        # Create commands.
        subparsers = parser.add_subparsers(title='Commands', dest='command')

        self._create_start_parser(subparsers)
        self._create_list_sources_parser(subparsers)
        self._create_list_filters_parser(subparsers)
        self._create_list_processors_parser(subparsers)
        self._create_list_transports_parser(subparsers)

        return parser

    def _execute_start(
        self,
        source: str,
        filter: str,
        processor: str,
        transport: str,
        config: Dict[str, str]
    ) -> None:
        # Construct video pipeline components.
        video_stream = get_video_stream(source)(config)
        frame_filter = get_frame_filter(filter)(config)
        video_processor = get_video_processor(processor)(config)
        video_transport = get_video_transport(transport)(config)
        output_handler = get_metrics_handler()(config)

        # Run the video pipeline.
        run_pipeline(
            video_stream,
            frame_filter,
            video_processor,
            video_transport,
            output_handler
        )

    def _run_setup(self, args: Optional[List[str]]) -> Namespace:
        # Parse CLI arguments.
        parsed_args = self._parser.parse_args() if args is None else self._parser.parse_args(args)

        # Set logging level.
        logger_handler = logging.StreamHandler(stream=sys.stdout)
        logger_handler.setFormatter(logging.Formatter('%(message)s'))
        logging.basicConfig(
            level=logging.INFO if parsed_args.verbose <= 0 else logging.DEBUG,
            handlers=[logger_handler]
        )

        # Logo.
        if not parsed_args.no_logo or os.environ.get('VP_NO_LOGO', '0') == '1':
            _logger.info(f'''
         _    __                 _          ___
   _  __(_)__/ /__ ___     ___  (_)__  ___ / (_)__  ___
  | |/ / / _  / -_) _ \\___/ _ \\/ / _ \\/ -_) / / _ \\/ -_)
  |___/_/\\_,_/\\__/\\___/  / .__/_/ .__/\\__/_/_/_//_/\\__/
                        /_/    /_/       v{__version__}
''')

        return parsed_args

    def run(self, args: Optional[List[str]]) -> int:
        # Parse provided args.
        parsed_args = self._run_setup(args)
        _logger.debug('Parsed Arguments:')
        _logger.debug(repr(parsed_args))

        if parsed_args.command == 'start':
            _logger.debug('Starting video-pipeline...')

            # Parse out pipeline configuration.
            config = parse_configuration(parsed_args.vars)
            config = dict(get_default_configuration(), **config)
            _logger.debug(repr(config))

            # Execute command.
            self._execute_start(
                parsed_args.source,
                parsed_args.filter,
                parsed_args.processor,
                parsed_args.transport,
                config
            )
            return 0

        if parsed_args.command == 'list-sources':
            _logger.info('Available Sources:')

            # Execute command.
            for source in list_video_streams():
                _logger.info(f'  {source}')
            return 0

        if parsed_args.command == 'list-filters':
            _logger.info('Available Filters:')

            # Execute command.
            for filter in list_frame_filters():
                _logger.info(f'  {filter}')
            return 0

        if parsed_args.command == 'list-processors':
            _logger.info('Available Processors:')

            # Execute command.
            for processor in list_video_processors():
                _logger.info(f'  {processor}')
            return 0

        if parsed_args.command == 'list-transports':
            _logger.info('Available Transports:')

            # Execute command.
            for transport in list_video_transports():
                _logger.info(f'  {transport}')
            return 0

        self._parser.print_help()
        return 1


def main() -> None:
    exit(VideoCli().run(None))


if __name__ == '__main__':
    main()
