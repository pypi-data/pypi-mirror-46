from video_pipeline.video_stream.video_frame_collector import VideoFrameCollector


def _construct_frame(format: str, image_data: bytes):
    frame_start_bytes = b''
    if format == 'mjpeg':
        frame_start_bytes = b'\xff\xd8\xff'

    if frame_start_bytes is None:
        raise AttributeError(f'format "{format}" not supported.')

    if image_data is None:
        return frame_start_bytes

    return frame_start_bytes + image_data


def test_write__mjpeg__unknown_size():
    # Given a video frame collector
    video_frame_collector = VideoFrameCollector(
        maxsize=10
    )

    # And a mjpeg frame in bytes format with unknown size
    frame_bytes = _construct_frame('mjpeg', b'\x00\x01\x02')

    # When the frame data is written to the video frame writer
    video_frame_collector.write(frame_bytes)

    # Then the frame data is written
    assert video_frame_collector._frame_buffer_stream.tell() > 0

    # Then no frames have buffered
    assert video_frame_collector._frame_buffer_queue.empty()


def test_write__mjpeg__complete_frame():
    # Given a video frame writer
    video_frame_collector = VideoFrameCollector(
        maxsize=10
    )

    # And a complete mjpeg frame in bytes format
    frame_bytes = _construct_frame('mjpeg', b'\x00\x01\x02')

    # When the frame data is written to the video frame collector
    video_frame_collector.write(frame_bytes)
    video_frame_collector.write(_construct_frame('mjpeg', None))

    # Then the complete frame is buffered
    frame = video_frame_collector._frame_buffer_queue.get_nowait()
    assert frame == b'\xff\xd8\xff\x00\x01\x02'

    # Then the incomplete frame data is written
    assert video_frame_collector._frame_buffer_stream.tell() > 0
