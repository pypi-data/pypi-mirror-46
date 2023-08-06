from unittest.mock import patch
from unittest.mock import MagicMock
from video_pipeline.video_transport.tcp_video_transport import TcpVideoTransport


def test_start():
    # Given a valid OS socket
    mock_socket = MagicMock()

    # And a TcpVideoTransport
    with patch(
        'video_pipeline.video_transport.tcp_video_transport.TcpVideoTransport._get_socket',
        new=MagicMock(return_value=mock_socket)
    ) as mock_get_socket:
        video_transport = TcpVideoTransport(mock_socket)

        # And a client connecting to that socket
        mock_client_socket = MagicMock()
        mock_socket.accept.return_value = (
            mock_client_socket, 'mock://0.0.0.0'
        )

        # When a video transport starts
        video_transport.start()

        # Then it should be running
        assert video_transport.is_running()

        # Then the socket established a client connection
        mock_get_socket.assert_called_once()
        mock_socket.accept.assert_called_once()
        mock_client_socket.makefile.assert_called_once()

        # Then the socket did not try to establish a server connection
        mock_socket.makefile.assert_not_called()


def test_stop():
    # Given a valid OS socket
    mock_socket = MagicMock()

    # And a running TcpVideoTransport connected to a client
    video_transport = TcpVideoTransport(mock_socket)
    video_transport._is_running = True
    video_transport._socket = MagicMock()
    video_transport._connection = MagicMock()

    # When a video transport stops
    video_transport.stop()

    # Then it should not be running
    assert not video_transport.is_running()

    # Then the socket and client connection are closed
    video_transport._socket.close.assert_called_once()
    video_transport._connection.close.assert_called_once()
