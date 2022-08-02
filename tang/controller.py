import json
import socket

from threading import Thread
from .rc4 import RC4
from .modules import InfoModule, CaptureModule

class Controller:
    """
    A single, self-contained instance of an API server.
    """

    """
    The number of threads this controller can create to receive simulatenous
    connections.
    """
    RECEIVING_THREAD_COUNT = 2

    """
    The maximum number of bytes that are received at once when reading from this
    controller's socket.
    """
    RECEIVING_DATA_SIZE = 64 * 1024

    def __init__(self, port, password=None):
        """
        Args:
            port (int): The port on the local machine to host this controller on.
            password (str): The password to use for encrypting data between this
                controller and its clients, if any.
        """

        if password:
            self.cipher = RC4(password.encode('utf-8'))
        else:
            self.cipher = None

        # create the socket
        self.address = ('0.0.0.0', port) #always open to the local network
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.is_open = False

        # configure the modules
        self.modules = {
            'info': InfoModule(),
            'capture': CaptureModule(),
        }

    def __del__(self):
        self.socket.close()

    def start(self):
        """
        Begin accepting connections to this controller.

        Notes:
            This method halts the calling thread until this controller's socket
            has closed.
        """

        # open the socket and spawn the receiving threads
        self.socket.listen()
        self.is_open = True

        self.receiving_threads = []
        for _ in range(Controller.RECEIVING_THREAD_COUNT):
            thread = Thread(target=self._receive_forever)
            thread.start()
            self.receiving_threads.append(thread)

        # log that the server is ready
        print(f'[controller] listening on port: {self.address[1]}')

        for thread in self.receiving_threads:
            thread.join()

    def close(self):
        """
        Close all existing connections to this controller's socket and close
        said socket.
        """

        # an ugly hack but functional
        # open split-second connections to satisfy the wait condition, thus
        # continuing the loops and checking is_open, which will then terminate
        # the threads properly
        # TODO: prevent logging these connections

        # log that this controller is closing to make it not so unclear why
        # connections are being logged
        print(f'[controller] closing...')

        self.is_open = False
        for _ in range(Controller.RECEIVING_THREAD_COUNT):
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(self.address)

        self.socket.close()

    def _receive_forever(self):
        """
        Receive connections from this controller's socket in an endless loop.
        """

        while self.is_open:
            # wait for connection
            connection, address = self.socket.accept()
            formatted_address = f'{address[0]}:{address[1]}'

            # receive data endlessly while the connection is open
            with connection:
                # log the connection
                print(f'[controller] client connected: {formatted_address}')

                is_connected = True
                message_buffer = bytearray(0)
                while is_connected:
                    # receive the next data block
                    data = connection.recv(Controller.RECEIVING_DATA_SIZE)

                    # if there is no data then the connection was closed
                    if not data:
                        break

                    # decrypt the data if encryption is being used
                    if self.cipher:
                        data = self.cipher.crypt(data)

                    for byte in data:
                        # check for the terminator to process the preceding data
                        if byte == 0x0:
                            request = json.loads(message_buffer.decode())
                            id = request['id']
                            module = request['module']
                            function = request['function']
                            parameters = request['params']

                            # log the request
                            formatted_parameters = ', '.join(map(lambda p: str(p), parameters))
                            print(f'[controller] request received ({id}): {module}.{function}({formatted_parameters})')

                            # construct the response fields
                            try:
                                module = self.modules[module]
                                function = getattr(module, function)
                                response_errors = []
                                response_data = function(*parameters)
                            except BaseException as error:
                                response_errors = [getattr(error, 'message', repr(error))]
                                response_data = []
                                is_connected = False

                            # log any errors for debugging
                            if response_errors:
                                for error in response_errors:
                                    print(f'[controller] error: {error}')

                            # construct and send the response
                            response = json.dumps({
                                'id': id,
                                'errors': response_errors,
                                'data': response_data,
                            }).encode('utf-8') + b'\0'

                            # encrypt the response if encryption is being used
                            if self.cipher:
                                response = self.cipher.crypt(response)

                            connection.send(response)

                            # wipe the buffer for the next request
                            message_buffer = bytearray(0)

                            # drop the connection if the server has decided to
                            if not is_connected:
                                connection.close()
                        else:
                            # continue building the next data to be processed
                            message_buffer.append(byte)

                # log the disconnection
                print(f'[controller] client disconnected: {formatted_address}')
