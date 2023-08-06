import pathlib

from setuptools import find_packages
from setuptools import setup

from video_pipeline import PROJECT_URL
from video_pipeline import __author__
from video_pipeline import __email__
from video_pipeline import __version__

README = (pathlib.Path(__file__).parent / 'README.md').read_text()

setup(
    name='video-pipeline',
    version=__version__,
    description='Simplify the video streaming pipeline to provide frame by frame image manipulation in near real-time.',  # noqa: E501
    long_description=README,
    long_description_content_type='text/markdown',
    url=PROJECT_URL,
    author=__author__,
    author_email=__email__,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='video pipeline filter visualization multiprocessing',
    packages=find_packages(exclude=['docs', 'tests']),
    project_urls={
        'Source': 'https://github.com/Nate-Wilkins/video-pipeline',
        'Changelog': 'https://github.com/Nate-Wilkins/video-pipeline/releases',
        'Documentation': 'https://Nate-Wilkins.github.io/video-pipeline/documentation',
    },
    include_package_data=False,
    install_requires=[
        'numpy',
        'filetype',
        'scikit-image',
        'imageio',
        'imageio-ffmpeg',
        'halo',
        'visvis'
    ],
    entry_points={
        'console_scripts': [
            'video-pipeline=video_pipeline.video_cli.__main__:main',
        ]
    },
)
