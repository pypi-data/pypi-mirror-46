import socket
import os
import tempfile
import enum
import itertools
import ssl
import socket as socketlib
import random
import collections
import unittest
import io
import inspect
import queue
import atexit
import trio

try:
    from dhttp import sslcert

except ImportError:
    import sslcert

try:
    import dhttp

except ImportError:
    import __init__ as dhttp



class CertMode(enum.Enum):
    CM_NONE = 0
    CM_GENERATED = 1
    CM_FILE = 2

class DequeBytesIO(io.IOBase):
    """
        A buffer-like object that can be
    truncated   and   written   to  from
    both  directions,  thanks to a Deque
    mechanism.
    """
    
    def __init__(self, data = None, cursor = 0):
        """
        Keyword Arguments:
            data {bytes} -- A bytes-like object with the which to initialize this buffer. (default: none)
            cursor {int} -- Where to initialize this buffer's cursor. (default: {0})
        """

        if data is None:
            self._buffer = collections.deque()

        else:
            self._buffer = collections.deque([self.ensure_bytes(data)])

        self.cursor = max(0, min(len(self), cursor))

    def ensure_bytes(self, data, string_mode=None):
        """
        Tries to obtain a bytes object from a bytes-like object.
        
        Arguments:
            data {any} -- A bytes or bytes-like object.
        
        Keyword Arguments:
            string_mode {str|None} --       Determines how to convert a string-like but
                                        not bytes-like object   into bytes;    'str' to
                                        encode str(data) into bytes,   and   'repr'  to
                                        encode repr(data) instead.
                                        (default: {None})
        
        Raises:
            TypeError -- Could not convert the given object into bytes.
        
        Returns:
            bytes -- The bytes version of the given object.
        """

        if isinstance(data, bytes):
            return data

        elif isinstance(data, bytearray):
            return bytes(data)

        elif isinstance(data, str):
            return data.encode('utf-8')

        elif string_mode == 'str':
            return str(data).encode('utf-8')

        elif string_mode == 'repr':
            return repr(data).encode('utf-8')

        else:
            raise TypeError("A bytes or byte-encodable value is required, not " + type(data).__name__ + "!")

    def index_at(self, position):
        remaining = position

        for index in range(len(self._buffer)):
            p = len(self._buffer[index])

            if p > remaining:
                return (index, remaining)

            else:
                remaining -= p

        return (index + 1, remaining)

    def buffer(self):
        """
        Returns an actual BytesIO buffer from
        the contents of this deque buffer.
        
        Returns:
            io.BytesIO -- The newly created buffer.
        """

        return io.BytesIO(self.read_all())

    def _get(self, ind):
        if ind < len(self._buffer):
            return self._buffer[ind]

        return b''

    def cap_position(self, pos):
        """
        Caps a given position value between 0 and len(buf).
        
        Arguments:
            pos {int} -- The position to be capped.
        
        Returns:
            int -- The capped position.
        """

        pos = int(pos)

        if pos < 0:
            pos = len(self) - pos

        return min(pos, len(self))

    def slice(self, start_pos = 0, end_pos = None):
        """
            Returns a slice of this buffer as a bytes object,
        which MAY then be used to create another buffer.
        
        Keyword Arguments:
            start_pos {int} -- The starting position of the slice. Defaults to the beginning of the buffer. (default: {0})
            end_pos {int|None} -- The end position of the slice. Defaults to the end of the buffer. (default: {None})
        
        Returns:
            bytes|None -- The data retrieved from the slice's range, or None if the range is out of bounds or of zero length.
        """

        if start_pos is None:
            start_pos = 0

        if end_pos is None:
            end_pos = len(self)

        start_pos = self.cap_position(start_pos)
        end_pos = self.cap_position(end_pos)

        if start_pos == end_pos:
            return None

        start = self.index_at(start_pos)
        end = self.index_at(end_pos)

        if start[0] == end[0]:
            return self._get(start[0])[start[1]:end[1]]
        
        else:
            res = b''

            if abs(start[0] - end[0]) > 1:
                for index in range(start[0] + 1, end[0]):
                    res += self._get(index)

            return self._get(start[0])[start[1]:] + res + self._get(end[0])[:end[1]]

    def __len__(self):
        """        
        Returns:
            int -- The number of bytes contained in this buffer.
        """

        return sum(len(x) for x in self._buffer)

    def remaining(self):
        """
        The length of data before the cursor.
        
        Returns:
            int -- You can guess.
        """

        return len(self) - self.cursor

    def cap_seek(self):
        self.seek(self.cursor) # automatically caps to content limits

    def truncate_right(self, amount = None):
        """
        Truncates this buffer from the right, i.e. starting at len(buf) - amount, and ending
        at len(buf).
        
        Keyword Arguments:
            amount {int} -- The amount of data to truncate. Defaults to everything from the cursor. (default: {None})
        """

        if amount is None:
            amount = self.cursor

        elif amount < 0:
            amount = len(self) - amount

        (tind, tpos) = self.index_at(amount)

        self._buffer = collections.deque(itertools.islice(self._buffer, tind))
        self.cap_seek()

        if len(self._buffer) > 0:
            self._buffer[-1] = self._buffer[-1][:tpos]

    def truncate(self, amount = None):
        """
        Buffer-compatible shorthand for truncate_left(amount).
        
        Keyword Arguments:
            amount {[type]} -- The amount of data to truncate. Defaults to everything up to the cursor. (default: {None})
        """

        self.truncate_left(amount)

    def truncate_left(self, amount = None):
        """
        Truncates this buffer from the left, i.e. starting at 0, and ending at amount.
        
        Keyword Arguments:
            amount {int} -- The amount of data to truncate. Defaults to everything up to the cursor. (default: {None})
        """
        if amount is None:
            amount = self.cursor
        
        elif amount < 0:
            amount = len(self) - amount

        (tind, tpos) = self.index_at(amount)

        self._buffer = collections.deque(itertools.islice(self._buffer, tind, None))
        self.seek_toward(-amount)

        if len(self._buffer) > 0:
            self._buffer[0] = self._buffer[0][tpos:]

    def __str__(self, encoding='utf-8'):
        return sum(self._buffer).decode(encoding)
    
    def __bytes__(self):
        return sum(self._buffer)

    def write(self, data, seek = False):
        """
        Writes to the right (or end) of this buffer.
        
        Arguments:
            data {bytes} -- Data to be written to the buffer.
        
        Keyword Arguments:
            seek {bool} -- Whether to move the cursor to the end of written data. (default: {False})
        """

        eb = self.ensure_bytes(data)
        self._buffer.append(eb)

        if seek:
            self.cursor += len(data)

        return eb

    def write_left(self, data):
        """
        Writes to the left (or start) of this buffer.
        
        Arguments:
            data {bytes} -- Data to be written to the start of the buffer.
        """

        self._buffer.appendleft(self.ensure_bytes(data))
        self.cursor += len(data)

    async def read_least(self, queue, size = None, pos = None, seek = True):
        """
        Read at least size bytes, no more, no less,   putting
        found data into a queue.
        
            If this size can't be initially reached, it waits
        (asynchronously).  This function only returns control
        (to any awaiting function)   once it has read exactly
        size bytes.
        
        Arguments:
            queue {queue.Queue} -- The queue to the which to put found data. Used to be able to fetch the data asynchronously.
        
        Keyword Arguments:
            size {int} -- The amount of data to be read. Defaults to every data immediately available before the cursor, i.e. doesn't wait. (default: {None})
            pos {int} -- The position at the which to read data. Defaults to the cursor. (default: {None})
            seek {bool} -- Whether to seek the cursor after reading. WILL seek before each wait. (default: {True})
        """


        if pos is None:
            pos = self.cursor

        if size is None:
            size = len(self) - pos

        wait_cursor = pos

        await trio.sleep(0.1)

        while True:
            d = self.slice(wait_cursor, pos + size)

            if d != b'':
                queue.put(d)
                wait_cursor += len(d)

            if seek:
                self.cursor = wait_cursor

            if wait_cursor >= pos + size:
                break
                
            await trio.sleep(0.05)

        queue.put(None)

    def read_all(self):
        """
        Reads all data in the buffer.
        
        Returns:
            bytes -- All data in the buffer! What else did you expect? :)
        """

        res = b''
        
        for data in self._buffer:
            res += data
        
        return res

    def read(self, size = None, pos = None, seek = True, truncate = False):
        """
        Reads and returns size bytes from the buffer.
        
        Keyword Arguments:
            size {int} -- The amount of bytes to be read. Defaults to everything immediately available before the cursor. (default: {None})
            pos {int} -- The position to be read from. Defaults to the cursor. (default: {None})
            seek {bool} -- Whether to seek the cursor to the end of read data after reading. (default: {True})
            truncate {bool} -- Whether to truncate read data in the buffer after reading. If True, the value of seek will be ignored. (default: {False})
        
        Returns:
            bytes -- The read data. :)
        """

        if pos is None:
            pos = self.cursor

        pos = self.cap_position(pos)

        if size is None:
            size = len(self) - pos
        
        data = self.slice(pos, pos + size)

        if data is None:
            return None

        if seek or truncate:
            self.seek_toward(len(data))

            if truncate:
                self.truncate()
        
        return data

    def seek(self, at):
        """
        Seeks the cursor
        
        Arguments:
            at {int} -- Whereat to seek the cursor.
        """

        self.cursor = self.cap_position(at)

    def seek_toward(self, at):
        """
        Seeks the cursor at bytes _forward_.
        
        Arguments:
            at {int} -- The offset or displacement by the wahich to move the cursor.
        
        Returns:
            int -- The new cursor position.
        """

        self.seek(at + self.tell())
        return self.tell()

    def tell(self):
        """
        Returns the position of the cursor.
        
        Returns:
            int
        """

        return self.cursor


class AsyncTCPClient(object):
    """
    A simple, but high-level TCP client.
    """

    def __init__(self):
        self.socket = None

        self._write_buffer = DequeBytesIO()
        self._receivers = set()

        self.running = False
        self.connected = False
        self.waiting = False

        self._on_close = set()

    def write(self, data):
        """
        Writes data to this TCP connection.
        
        Arguments:
            data {bytes} -- A bytes-like data value to be sent.
        """

        self._write_buffer.write(data)

    def on_close(self, f):
        self._on_close.add(f)
        return f

    def receiver(self, func):
        """
        Adds the argument function as a receiver, which is
        called everytime data is received. The handler function
        MAY be an asynchronous function.
        
        Arguments:
            func {function} -- The method 'receiver' may be used as a decorator.
        """
        self._receivers.add(func)
        return func

    async def _recv(self, data):
        async def sync_handler(r, data):
            r(data)

        async with trio.open_nursery() as nursery:
            for r in self._receivers:
                if inspect.iscoroutinefunction(r):
                    nursery.start_soon(r, data)

                else:
                    nursery.start_soon(sync_handler, r, data)

    def stop(self):
        """
        Stops this client's main loop, if it is running.
        """

        self.running = False

    async def loop(self):
        """
        Starts this client's main loop, if it is not yet running.
        """

        if self.running:
            raise ConnectionError("This client is already running!")

        self.running = True
        unsent = 0
        
        if not self.connected:
            self.waiting = True

            while not self.connected:
                if not self.running:
                    self.socket = None
                    return

                await trio.sleep(1 / 8)

            self.waiting = False

        while self.running or unsent > 0:
            sleep_amount = 1 / 30

            if self.running:
                try:
                    data = self.socket.recv(1024)

                    if data == b'':
                        self.stop()
                        break

                    else:
                        await self._recv(data)

                except ConnectionResetError:
                    self.stop()
                    break

                except (BlockingIOError, ssl.SSLWantReadError):
                    sleep_amount = 1 / 20

                except ssl.SSLError as err:
                    print(dhttp.DHTTPGenericLog('ERR', f'(SSL CLIENT: {type(err).__name__}) {str(err)}'))
                    break
            
            if not self.running:
                read_amount = min(1024, unsent)

            else:
                read_amount = 1024

            write_data = self._write_buffer.read(read_amount, seek = False)

            if write_data is not None:
                sent = self.socket.send(write_data)
                self._write_buffer.truncate(sent)
                unsent = max(0, unsent - sent) + max(0, len(write_data) - sent)

            await trio.sleep(sleep_amount)

        # self.socket.shutdown(socketlib.SHUT_RDWR)
        self.socket.close()

        async def sync_handler(f):
            f()

        async with trio.open_nursery() as nursery:
            for f in self._on_close:
                if inspect.iscoroutinefunction(f):
                    nursery.start_soon(f)

                else:
                    nursery.start_soon(sync_handler, f)

        self.socket = None
        self.connected = False

    async def connect(self, host, port, tls = False, cert_mode = CertMode.CM_GENERATED, cert_file = None, key_file = None, key_size = 2048):
        """
        Connects to a given TCP host and port.
        
        Arguments:
            host {str} -- The host to connect to.
            port {int} -- The port to connect to.
            tls {bool} -- Whether to use TLS/SSL. (default: {False})
            cert_mode {CertMode} -- Defines a certificate mode. May be none, CM_GENERATED (for a generated certificate), or CM_FILE. (default: {CertMode.CM_NONE})
            cert_file {str} -- A path to a PEM certificate file. Supply only if the value of 'cert_mode' is not CM_NONE and tls is True (default: {None})
            key_file {str} -- A path to a PEM key file. Supply only if the value of 'cert_mode' is not CM_NONE and tls is True. (default: {None})
            key_size {int} -- The size of a CM_GENERATED RSA key. Unused argument if tls is False or cert_mode isn't CM_GENERATED. (default: {2048})
        """
        if self.connected:
            raise ConnectionError("This client is already connected!")

        else:
            self.socket = socketlib.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

            if tls:
                if cert_mode is None:
                    # still not sure whether to replace CertMode.CM_NONE by None in the future
                    cert_mode = CertMode.CM_NONE

                context = ssl.SSLContext(ssl.PROTOCOL_TLS)

                if cert_mode != CertMode.CM_NONE:
                    if cert_file is None or key_file is None:
                        raise ValueError("tls is True and cert_mode is not CM_NONE, but cert_file and/or key_file are None!")

                    else:
                        if cert_mode == CertMode.CM_GENERATED:
                            sslcert.self_signed_cert(cert_file, key_file)

                        context.load_cert_chain(cert_file, key_file)

                context.verify_mode = ssl.CERT_NONE

                self.socket = context.wrap_socket(self.socket, server_hostname = host)

            self.socket.connect((host, port))
            self.socket.setblocking(False)

            self.connected = True

    async def run_connect(self, host, port, *args, **kwargs):
        """
        Connects to a given TCP host and port, and runs
        the main loop. Accepts extra connect arguments.
        
        Arguments:
            host {str} -- The host to connect to.
            port {int} -- The port to connect to.
        """

        self.connect(host, port, *args, **kwargs)
        await self.loop()


class AsyncTCPServer(object):
    """
    A TCP server running on trio.
    """


    class Client(object):
        """
        A client to a TCP server.
        """

        def __init__(self, server, socket, addr):
            self.server = server
            self.address = addr
            self.socket = socket

            self.out_buffer = DequeBytesIO()

            self._pending_close = False
            self.closed = False

            self._on_close = set()
            self.reset_receivers()

        def on_close(self, f):
            self._on_close.add(f)
            return f

        def remove_handler(self, f):
            if f in self._receivers:
                self._receivers.remove(f)

            if f in self._on_close:
                self._on_close.remove(f)

        def reader(self):
            """
            Returns a new reader, i.e. a buffer that is
            written everytime this socket receives data.
            
            Returns:
                DequeBytesIO -- The new reader buffer.
            """

            reader = DequeBytesIO()

            @self.receiver
            async def _write_to_reader(_, data):
                reader.write(data)

            return reader

        def reset_receivers(self):
            """
            Resets the 'index' of TCP receiving callbacks.
            """

            self._receivers = set()

        def verify_close(self):
            if self.closed:
                raise TCPClientError("The client socket was already closed!")

        def receiver(self, func):
            """
            Adds a TCP receiving callback to this TCP client.
            Can be used as a decorator.
            """

            async def _receiver_callback(_, data):
                if inspect.iscoroutinefunction(func):
                    await func(data)

                else:
                    func(data)

            self._receivers.add(_receiver_callback)
            return _receiver_callback

        def write(self, data):
            """
            Writes to this TCP client.
            
            Arguments:
                data {bytes} -- The data to be written to this TCP client.
            """
            self.verify_close()
            self.out_buffer.write(data)

        def close(self):
            """
            Closes this TCP client safely.
            """

            self._pending_close = True

        async def _close(self):
            if not self.closed:
                # self.socket.shutdown(socketlib.SHUT_RDWR)
                self.socket.close()

            async def sync_handler(f): 
                f(self)

            async with trio.open_nursery() as nursery:
                for f in self._on_close:
                    if inspect.iscoroutinefunction(f):
                        nursery.start_soon(f, self)

                    else:
                        nursery.start_soon(sync_handler, f)
                
            self.closed = True

        async def receive(self, data):
            if data == b'':
                await self._close()

            else:
                async def sync_handler(f): 
                    f(self, data)

                async with trio.open_nursery() as nursery:
                    for f in self._receivers | self.server._receivers:
                        if inspect.iscoroutinefunction(f):
                            nursery.start_soon(f, self, data)

                        else:
                            nursery.start_soon(sync_handler, f)

    def __init__(self):
        self._on_accept = set()
        self._receivers = set()

        self.running = False

    def stop(self):
        """
        Stops this TCP server.
        """

        self.running = False

    def reset_receivers(self):
        """
        Resets the global 'index' of TCP receiving callbacks.
        """

        self._receivers = set()

    def receiver(self, func):
        """
        Adds a receiver function to every next
        Client object spawned by this server.
        
        Arguments:
            func {function} -- The handler function. This argument can be used to decorate.
        """

        self._receivers.add(func)
        return func

    def on_accept(self, func):
        """
        Adds a handler to be called everytime a Client object is generated from this server..
        
        Arguments:
            func {function} -- The handler function. This argument can be used to decorate.
        """

        self._on_accept.add(func)

        return func

    async def serve(self, client):
        """
        This function can be overriden in subclasses
        to serve a new Client object before other
        handlers are called.
        
        Arguments:
            client {AsyncTCPServer.Client} -- The Client object.
        """

        pass

    def _wrap_client(self, socket, addr):
        """
        Wraps a TCP socket and an address value in a
        Client object.
        
        Arguments:
            socket {socket.socket} -- The client socket.
            addr {Tuple[str,str]} -- The client's Internet address.
        """

        client = AsyncTCPServer.Client(self, socket, addr)

        return client

    async def _accept(self, socket, addr):
        client = self._wrap_client(socket, addr)

        async def sync_handler(h):
            h(client)

        async with trio.open_nursery() as nursery:
            nursery.start_soon(self._run_client, client)
            nursery.start_soon(self.serve, client)

            for f in self._on_accept:
                if inspect.iscoroutinefunction(f):
                    nursery.start_soon(f, client)

                else:
                    nursery.start_soon(sync_handler, f)

    async def _run_client(self, client):
        client.socket.setblocking(False)

        unsent = 0

        while (not client.closed) and self.running:
            sleep_amount = 1 / 35

            try:
                if not client._pending_close:
                    data = client.socket.recv(1024)

                    if data == b'':
                        client.close()
                        break

                    await client.receive(data)

                else:
                    sleep_amount = 1 / 25

                if client.closed:
                    break

            except ConnectionResetError:
                client.close()
                break

            except (BlockingIOError, ssl.SSLWantReadError):
                sleep_amount = 1 / 15

            except ssl.SSLError as err:
                print(dhttp.DHTTPGenericLog('ERR', f'(SSL SERVER: {type(err).__name__}) {str(err)}'))
                client.close()
                break
            
            if client.closed or not self.running:
                break

            if client.out_buffer.remaining() > 0:
                data = client.out_buffer.read(1024, seek = False)
                sent = client.socket.send(data)

                client.out_buffer.seek_toward(sent)
                client.out_buffer.truncate_left(sent)

                unsent = max(0, unsent - sent) + max(0, len(data) - sent)

                sleep_amount *= 0.9

            else:
                if client._pending_close:
                    await client._close()

            await trio.sleep(sleep_amount)

        if not client.closed:
            await client._close()
        
    async def run(self, port, host='0.0.0.0', tls = False, cert_mode = CertMode.CM_GENERATED, cert_file = None, key_file = None, key_size = 2048):
        """
        This asynchronous function runs the server.
        
        Arguments:
            port {int} -- The port on the which to run the server.
        
        Keyword Arguments:
            host {str} -- The source hostname on the which to listen for connections. (default: {'0.0.0.0'})
            tls {bool} -- Whether to use TLS/SSL. (default: {False})
            cert_mode {CertMode} -- Defines a certificate mode. May be none, CM_GENERATED (for a generated certificate), or CM_FILE. (default: {CertMode.CM_NONE})
            cert_file {str} -- A path to a PEM certificate file. Supply only if the value of 'cert_mode' is CM_FILE. (default: {None})
            key_file {str} -- A path to a PEM key file. Supply only if the value of 'cert_mode' is CM_FILE. (default: {None})
            key_size {int} -- The size of a CM_GENERATED RSA key. Unused argument if tls is False or cert_mode isn't CM_GENERATED. (default: {2048})
        """

        self.running = True

        listen_socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)

        key_fp = None
        cert_fp = None

        if tls:
            if cert_mode is None:
                # still not sure whether to replace CertMode.CM_NONE by None in the future
                cert_mode = CertMode.CM_NONE

            context = ssl.SSLContext(ssl.PROTOCOL_TLS)

            if cert_mode != CertMode.CM_NONE:
                if cert_file is None or key_file is None:
                    raise ValueError("tls is True and cert_mode is not CM_NONE, but cert_file and/or key_file are None!")

                else:
                    if cert_mode == CertMode.CM_GENERATED:
                        sslcert.self_signed_cert(cert_file, key_file)

                    context.load_cert_chain(cert_file, key_file)

            context.verify_mode = ssl.CERT_NONE
            listen_socket = context.wrap_socket(listen_socket, server_side = True)

        listen_socket.bind((host, port))
        listen_socket.listen(5)
        listen_socket.setblocking(False)

        async with trio.open_nursery() as nursery:
            _run = True

            @atexit.register
            def _at_exit():
                if _run:
                    self.running = False
                    # listen_socket.shutdown(socketlib.SHUT_RDWR)
                    listen_socket.close()
            
            listen_socket.setblocking(False)

            while self.running:
                try:
                    while self.running:
                        try:
                            (socket, addr) = listen_socket.accept()

                        except BlockingIOError:
                            await trio.sleep(1 / 15)

                        else:
                            nursery.start_soon(self._accept, socket, addr)
                            sleep_amount = 0.1

                            break

                except ConnectionResetError:
                    self.stop()
                    break

                except (BlockingIOError, ssl.SSLWantReadError):
                    sleep_amount = 0.25

                except ssl.SSLError as err:
                    print(dhttp.DHTTPGenericLog('ERR', f'(SSL LISTEN: {type(err).__name__}) {str(err)}'))
                    sleep_amount = 0.1
                    break

                if not self.running:
                    break

                await trio.sleep(sleep_amount)

            _run = False
            # listen_socket.shutdown(socketlib.SHUT_RDWR)
            listen_socket.close()

    def run_forever(self, port, host='127.0.0.1'):
        trio.run(self.run, port, host)


class TCPClientError(BaseException):
    pass


#===


class EchoServerTest(object):
    async def run_serv(self, callback):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.server.run, self.port)
            nursery.start_soon(callback)

    def __init__(self, port = None):
        if port is None:
            port = random.randint(7000, 7999)

        self.port = int(port)
        self.server = AsyncTCPServer()

        @self.server.receiver
        async def receive(client, data):
            client.write(data + data)

        class EchoServerTestCase(unittest.TestCase):
            def test_double_echo(case):
                async def run():
                    async def run_test():
                        cl = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)

                        connected = False
                        while not connected:
                            try:
                                cl.connect(('127.0.0.1', self.port))
                                connected = True

                            except socket.error:
                                await trio.sleep(0.2)

                        cl.sendall(b'MyTest')
                        cl.setblocking(False)

                        data = b''

                        while True:
                            try:
                                nd = cl.recv(1024)

                                if nd == b'':
                                    break

                                else:
                                    data += nd

                                    # cl.shutdown(socketlib.SHUT_RDWR)
                                    cl.close()

                                    await trio.sleep(0.1)
                                    break

                            except ConnectionResetError:
                                self.stop()
                                break

                            except (BlockingIOError, ssl.SSLWantReadError):
                                await trio.sleep(0.2)

                        case.assertEqual(len(data), 2 * len(b'MyTest'))
                        case.assertEqual(data, b'MyTestMyTest')

                        self.server.stop()

                    async def callback():
                        await run_test()

                    await self.run_serv(callback)

                trio.run(run)

            def test_read_least(case):
                print()
                buf = DequeBytesIO()

                async def put_wait():
                    def write(data):
                        buf.write(data)
                        print(' --> ', data)

                    write(b'A')
                    await trio.sleep(0.3)
                    write(b'BC')
                    await trio.sleep(1.2)
                    write(b'DEF')
                    await trio.sleep(1)
                    write(b'GHI')
                    await trio.sleep(1.5)
                    write(b'JKL')

                async def read_wait():
                    q = queue.Queue()
                    res = b''
                    waits = 0

                    async with trio.open_nursery() as nursery:
                        nursery.start_soon(buf.read_least, q, 8)
                        await trio.sleep(0.1)

                        while True:
                            if not q.empty():
                                data = q.get_nowait()

                                if data is None:
                                    break

                                else:
                                    res += data
                                    waits += 1

                                print(data, res)

                            await trio.sleep(0.25)

                        print()
                        print('-----')
                        print()
                        print('result:', res)
                        print()
                        print('-----')

                        case.assertEqual(len(res), 8)
                        case.assertEqual(res, b'ABCDEFGH')
                        case.assertEqual(waits, 4)

                async def run_test():
                    async with trio.open_nursery() as nursery:
                        nursery.start_soon(read_wait)
                        nursery.start_soon(put_wait)

                trio.run(run_test)

        self.TestCase = EchoServerTestCase

    def run(self):
        unittest.main(self.TestCase())

if __name__ == "__main__":
    EchoServerTest().run()