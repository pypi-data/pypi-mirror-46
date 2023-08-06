# Video Pipeline

[![version](https://img.shields.io/pypi/v/video-pipeline.svg?style=for-the-badge)](https://pypi.org/project/video-pipeline/) [![Documentation](https://readthedocs.org/projects/video-pipeline/badge/?version=latest&style=for-the-badge)](https://video-pipeline.readthedocs.io/en/latest/?badge=latest) [![license](https://img.shields.io/pypi/l/video-pipeline.svg?style=for-the-badge)](https://github.com/Nate-Wilkins/video-pipeline/blob/master/LICENSE) ![status](https://img.shields.io/travis/Nate-Wilkins/video-pipeline/master.svg?style=for-the-badge) [![issues](https://img.shields.io/github/issues/Nate-Wilkins/video-pipeline.svg?style=for-the-badge)](https://github.com/Nate-Wilkins/video-pipeline/issues)

> Simplify the video streaming pipeline to provide frame by frame image manipulation in near real-time.

## Abstract

Video streaming and image processing are really interesting!

This package aims to simplify the video streaming pipeline so users can focus on the more interesting parts of image processing.
To learn more about how this is accomplished and the details that make up the pipeline see the [docs](https://video-pipeline.readthedocs.io/en/latest/).

## Getting Started

The `video-pipeline` comes with a command line interface (CLI) that you can utilize to preview, transport, and/or modify video streams!

1. First you need to install the `video-pipeline` module from PyPI by running:

    ```bash
    pip install video-pipeline
    ```

2. Once installed `video-pipeline` should be on your `PATH`.

3. Make sure you have [vlc](https://www.videolan.org/vlc/index.html) installed and on your `PATH`.

4. Run the following command to start streaming video from your webcam:

    ```bash

    video-pipeline start --source os --transport tcp-server transport-host=0.0.0.0 transport-port=8000
    ```

5. On the same computer (or another computer on your LAN) run the following command replacing `HOSTNAME` with the hostname of the computer running `video-pipeline`.

    __Note__: If you're running on a linux machine you can run `hostname` to get your `HOSTNAME`.

    ```bash
    vlc "tcp/mjpeg://@HOSTNAME:8000/"
    ```

6. You should now see a stream of your webcam!

To learn more about the `video-pipeline` command line interface run `video-pipeline --help`.

If you have any issues questions, comments, or concerns please feel free to submit an issue to the [issue tracker](https://github.com/Nate-Wilkins/video-pipeline/issues).

[//]: # (TODO@pl: Combine multiple README here and in docs/)
