import io
import logging
import socket
import struct
import imageio
from typing import Optional

import numpy as np

from video_pipeline.video_transport import VideoTransport

_logger = logging.getLogger(__name__)


class TcpVideoTransportConnectionError(Exception):
    """Indicates that the tcp video transport ran into a connection issue.
    """


class TcpVideoTransport(VideoTransport):
    _socket_host: str
    _socket_port: int
    _is_server: bool
    _socket: Optional[socket.socket]
    _connection: Optional[io.BytesIO]

    def __init__(
        self,
        socket_host: str,
        socket_port: int = 8000,
        is_server: bool = True,
        # TODO@nw: Support multiple formats...
        video_format: str = 'JPEG-PIL'
    ) -> None:
        super().__init__()

        self._socket_host = socket_host
        self._socket_port = socket_port
        self._is_server = is_server
        self._stream = io.BytesIO()
        self._socket = None
        self._connection = None
        self._video_format_conversion = video_format

    def _get_socket(self) -> socket.socket:
        """Sets up a socket for communication by grabbing the first
        address family available.

        External Resources:
        - https://docs.python.org/3/library/socket.html
        """
        target_socket = None

        for res in socket.getaddrinfo(
            self._socket_host,
            self._socket_port,
            socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        ):
            af, socktype, proto, _canonname, sa = res

            # Create a new socket for this address.
            try:
                target_socket = socket.socket(af, socktype, proto)

                # Indicate that we can reuse the address if it was used previously.
                target_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except OSError:
                target_socket = None
                continue

            # Connect to the target socket.
            try:
                if self._is_server:
                    target_socket.bind(sa)
                    target_socket.listen(1)
                else:
                    target_socket.connect(
                        (self._socket_host, self._socket_port)
                    )
            except OSError:
                target_socket.close()
                target_socket = None
                continue

            # Found a suitable socket.
            break

        if target_socket is None:
            raise ValueError(
                f'Unable to open socket on "{self._socket_host}:{self._socket_port}". Is it already in use?'  # noqa: E501
            )

        return target_socket

    def _start_transport(self) -> None:
        self._socket = self._get_socket()
        if self._is_server:
            client_connection, client_address = self._socket.accept()
            _logger.debug(f'Client {client_address} connected!')

            self._connection = client_connection.makefile('wb')
        else:
            self._connection = self._socket.makefile('wb')

    def _stop_transport(self) -> None:
        if self._connection is None or self._socket is None:
            raise TcpVideoTransportConnectionError(
                '"connection" invalid. Make sure to start the transport.'
            )

        try:
            if not self._is_server:
                # Indicate to the server that we have nothing more to send.
                self._connection.write(struct.pack('<L', 0))
        finally:
            self._connection.close()
            self._socket.close()

    def _transport_frame(self, frame: np.array) -> None:
        if self._connection is None:
            raise TcpVideoTransportConnectionError(
                '"connection" invalid. Make sure to start the transport.'
            )

        try:
            # The imsave does not provide safe signature types, indicate bytes.
            image_data: bytes = imageio.imsave(
                imageio.RETURN_BYTES,
                frame,
                format=self._video_format_conversion
            )

            if not self._is_server:
                # Inform to the server how much data we're going to send.
                self._connection.write(struct.pack('<L', len(image_data)))
                self._connection.flush()

            # Send frame image data.
            self._connection.write(image_data)
        except Exception as e:
            raise TcpVideoTransportConnectionError() from e
