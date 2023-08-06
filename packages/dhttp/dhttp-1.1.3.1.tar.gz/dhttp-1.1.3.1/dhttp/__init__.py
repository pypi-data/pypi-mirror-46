# -*- coding: utf-8 -*-
import functools
import itertools
import random
import enum
import warnings
import struct
import inspect
import binascii
import trio
import urllib
import jinja2
import asyncio
import sys
import fnmatch
import datetime
import os
import traceback
import mimetypes
import re
import hashlib
import base64
import io
import abc
import collections

from . import tcp
from .dhttpversion import DHTTP_VERSION

tcpserver = tcp


# ==== BASIC WEBSOCKET INFRASTRUCTURE ====

# --- Opcode List Enum

class WSOpcode(enum.Enum):
    CONTINUE = 0
    TEXT = 1
    BINARY = 2
    UNKNOWN_3 = 3
    UNKNOWN_4 = 4
    UNKNOWN_5 = 5
    UNKNOWN_6 = 6
    UNKNOWN_7 = 7
    CLOSE = 8
    PING = 9
    PONG = 10
    CONTROL_B = 11
    CONTROL_C = 12
    CONTROL_D = 13
    CONTROL_E = 14
    CONTROL_F = 15

    @staticmethod
    def control(opcode):
        return bool(opcode.value & 0x8)

# --- Opcode Action Metaclass

class WSOpcodeTypeMeta(type):
    """
    This metaclass is responsible for
    registering    WebSocket   opcode
    actions.
    """

    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if hasattr(self, 'OPCODE'):
            opcode = self.OPCODE
            getattr(WSOpcodeTypeIndex, opcode).add(self)

class WSOpcodeTypeIndex(object):
    actions = {}

    def get_actions(self, opcode):
        return type(self).actions.get(opcode, set())
    
    async def server_handle_message(self, server, client, message):
        async with trio.open_nursery() as nursery:
            for a in self.get_actions(message.opcode):
                nursery.start_soon(a.server_handle_message, server, client, message)

    async def client_handle_message(self, client, message):
        async with trio.open_nursery() as nursery:
            for a in self.get_actions(message.opcode):
                nursery.start_soon(a.client_handle_message, client, message)

WSOpcodeTypes = WSOpcodeTypeIndex()

for opc in WSOpcode:
    WSOpcodeTypeIndex.actions[opc] = set()

# --- Byte Stream Wrapping Utility for WebSockets (BSWU-WS)

class WSByteStreamWrapperMixin(object):
    def _init_wrapped(self, base_class, mask = True, server = None):
        self.base_class = base_class
        self.mask = mask

        # assuming this class supports the Receiver Callback API
        if hasattr(self, 'receiver'):
            self._ws_receivers = set()
            self._ws_buffer = b''

            @self.receiver
            async def _ws_receive_data(data):
                packets = WSPacket.decode(self._ws_buffer + data)
                self._ws_buffer = packets.tail

                for p in packets.packets:
                    if server is None:
                        await WSOpcodeTypes.client_handle_message(self, p)

                    else:
                        await WSOpcodeTypes.server_handle_message(server, self, p)

                async def sync_handler(r, p):
                    r(p)

                async with trio.open_nursery() as nursery:
                    for p in packets.packets:
                        if not WSOpcode.control(p.opcode):
                            for r in self._ws_receivers:
                                if inspect.iscoroutinefunction(r):
                                    nursery.start_soon(r, p)

                                else:
                                    nursery.start_soon(sync_handler, r, p)

        else:
            self._ws_receivers = None

    def ws_receiver(self, func):
        if self._ws_receivers is None:
            raise TypeError('The base class {bcname} does not support the Receiver Callback API!'.format(bcname = self.base_class.__name__))

        else:
            self._ws_receivers.add(func)
            return func

    def ws_send(self, opcode = WSOpcode.BINARY, content = None, mask = None, final = True):
        message = WSPacket(final, opcode, content, mask)
        encoded = message.encode()

        self.write(encoded)
        return encoded

    def ws_write(self, data):
        if isinstance(data, str):
            opcode = WSOpcode.TEXT
            data = bytearray(data, 'utf-8')

        elif isinstance(data, bytes) or isinstance(data, bytearray):
            opcode = WSOpcode.BINARY
            data = bytearray(data)

        else:
            raise ValueError("'data' must be either str, bytes or bytearray; got {datatype} instead!".format(datatype = type(data).__name__))

        message = WSPacket(True, opcode, data, mask = (None if bool(self.mask) else False))

        self.write(message.encode())

        return message

    def ws_send_packet(self, packet):
        encoded = packet.encode()

        self.write(encoded)
        return encoded

    def ws_close(self):
        self.ws_send_packet(WSPacket(opcode = WSOpcode.CLOSE, mask = (None if bool(self.mask) else False)))
        self.close()

def wrap_websocket(o, server = None, mask = True):
    t = type(o)

    o._receivers = set()
    o.__class__ = type('_WSWU_' + t.__name__, (t, WSByteStreamWrapperMixin), {})
    o._init_wrapped(t, mask, server)

    return o

# --- Opcode Actions

class WSOpcodeType(abc.ABC):
    @abc.abstractclassmethod
    async def server_handle_message(cls, server, client, message):
        pass

    @abc.abstractclassmethod
    async def client_handle_message(cls, client, message):
        pass

class WSPingOpcodeType(WSOpcodeType):
    OPCODE = WSOpcode.PING

    @classmethod
    async def server_handle_message(cls, server, client, message):
        client.ws_send(True, WSOpcode.PONG, message.content, message.mask)

    @classmethod
    async def client_handle_message(cls, client, message):
        client.ws_send(True, WSOpcode.PONG, message.content, message.mask)

class WSCloseOpcodeType(WSOpcodeType):
    OPCODE = WSOpcode.CLOSE

    @classmethod
    async def server_handle_message(cls, server, client, message):
        client.close()

    @classmethod
    async def client_handle_message(cls, client, message):
        client.close()

# --- Packets

LONG_LONG_MASK = (1 << 64) - 1

WSDecodedPackets = collections.namedtuple('WSDecodedPackets', ('packets', 'tail'))

def error_default(func, error_type, default, *args, **kwargs):
    def _inner():
        try:
            return func(*args, **kwargs)

        except error_type:
            return default

    return _inner

class WSBasePacketStream(io.IOBase):
    def readline(self, _):
        raise NotImplementedError("Operation 'readline' not supported in a WebSocket packet stream.")

    def readlines(self, _):
        raise NotImplementedError("Operation 'readline' not supported in a WebSocket packet stream.")

    def writelines(self, _):
        raise NotImplementedError("Operation 'readline' not supported in a WebSocket packet stream.")

    def isatty(self, _):
        return False
        
    def seekable(self):
        return False

    def fileno(self):
        raise OSError("WebSocket streams do not use a file descriptor.")

class WSPacketReadStream(WSBasePacketStream):
    def __init__(self):
        self.data = tcpserver.DequeBytesIO()

    def read(self, size = None):
        if size is None:
            return self.data.read(truncate = True)

class WSPacketWriteStream(WSBasePacketStream):
    def __init__(self, mask = None):
        self.mask = mask
        self.packets = []

    def read(self, packets = 1):
        if packets > 1:
            return itertools.islice(iter(error_default(self.packets.pop, IndexError, None, 0), None), packets)
        
        else:
            return self.packets.pop(0)

    def readable(self):
        return True

    def close(self, rsv):
        self.write_packets(WSPacket(rsv = rsv))
        super().close()

    def write_packets(self, *packets):
        for p in packets:
            self.packets.append(p)

    def write_raw(self, encoded):
        decoded = WSPacket.decode(encoded)

        for d in decoded.packets:
            self.write_packets(d)

        return len(encoded) - len(decoded.tail)

    def write(self, data, rsv):
        self.write_packets(WSPacket(fin = False, content = data, mask = self.mask, rsv = rsv))


class WSPacket(object):
    def __init__(self, fin = True, opcode = WSOpcode.BINARY, content = None, mask = None, rsv = 0):
        self.fin = fin
        self.rsv = rsv
        self.opcode = opcode

        if content is None:
            self.content = b''
            self.mask = None

        else:
            if isinstance(content, str):
                content = bytearray(content.encode('utf-8'))

            self.content = content

            if mask is None:
                self.mask = struct.pack('4B', *[random.randint(0, 255) for _ in range(4)])

            elif mask is False:
                self.mask = None

            else:
                self.mask = mask[:4] + bytearray((0,)) * max(0, 4 - len(mask))

    def __len__(self):
        return len(self.content)

    def __repr__(self):
        return f"WSPacket(fin={self.fin} rsv={bin(self.rsv).zfill(3)} mask={self.mask.hex()} opcode={self.opcode.name} len={len(self)})"

    def encode(self):
        opcode = self.opcode

        if isinstance(opcode, WSOpcode):
            opcode = opcode.value

        data = bytearray(struct.pack('B', int(self.fin) << 7 | (self.rsv & 0x7) << 4 | self.opcode.value))

        if len(self) > pow(2, 16):
            length_field = struct.pack('Q', len(self) & LONG_LONG_MASK)
            length_bits = 127

        elif len(self) > 125:
            length_field = struct.pack('H', len(self))
            length_bits = 126

        else:
            length_field = b''
            length_bits = len(self) & 0x7F

        data += struct.pack('B', ((self.mask != None) << 7) | length_bits) + length_field

        if self.mask is not None:
            data += bytearray(self.mask) + bytearray(d ^ self.mask[i % 4] for i, d in enumerate(self.content))

        else:
            data += self.content

        return data

    @classmethod
    def decode(self, data):
        if isinstance(data, str):
            data = bytearray(data, 'utf-8')

        else:
            data = bytearray(data)

        messages = []
        tail = bytearray(data)

        while True:
            remaining = bytearray(tail)

            if len(remaining) < 3:
                break

            fo = remaining.pop(0)
            ml = remaining.pop(0)

            fin = bool(fo & 0x80)
            rsv = fo & 0x70 >> 4
            opcode = WSOpcode(fo & 0xF)
            masked = bool(ml & 0x80)

            l = ml & 0x7F

            if l == 126:
                if len(remaining) < 2:
                    break

                l = struct.unpack('H', remaining[:2])[0]
                remaining = remaining[2:]

            elif l == 127:
                if len(remaining) < 8:
                    break
                
                l = struct.unpack('Q', remaining[:8])[0]
                remaining = remaining[8:]

            if masked:
                if len(remaining) < 4:
                    break

                mask = remaining[:4]
                remaining = remaining[4:]

            else:
                mask = None

            if len(remaining) < l:
                break

            content = remaining[:l]
            remaining = remaining[l:]

            if mask is not None:
                content = bytearray(b ^ mask[i % 4] for i, b in enumerate(content))

            if opcode == WSOpcode.TEXT:
                content = content.decode('utf-8')

            pkt = WSPacket(fin, opcode, content, mask, rsv)
            messages.append(pkt)
            tail = remaining

        return WSDecodedPackets(messages, tail)

#========================

def read(fname):
    fp = open(os.path.join(os.path.dirname(__package__), fname))
    data = fp.read()
    fp.close()

    return data

DHTTPCallback = collections.namedtuple('DHTTPCallback', ('headers', 'callback'))


class DHTTPLog(abc.ABC):
    def __init__(self):
        self.when = datetime.datetime.utcnow()

    @abc.abstractmethod
    def log_type(self):
        pass

    @abc.abstractmethod
    def log_data(self):
        pass

    def __str__(self):
        return f'[{self.when.strftime("%Y-%m-%d %H:%M:%S")}]   {("(" + self.log_type() + ")").ljust(15)} {self.log_data()}'

    def __iter__(self):
        return iter((self.log_type(), self.log_data()))


class DHTTPGenericLog(DHTTPLog):
    def __init__(self, kind, message):
        super().__init__()

        self.kind = kind
        self.message = message

    def log_type(self):
        return self.kind

    def log_data(self):
        return self.message


class DHTTPRequestLog(DHTTPLog):
    def __init__(self, method, ip, request_path, request):
        super().__init__()

        self.method = method
        self.ip = ip
        self.request_path = request_path
        self.request = request

    def log_type(self):
        return 'HTTP: ' + self.method

    def log_data(self):
        return f'{self.ip} @ {self.request_path}'


class DHTTPRequest(object):    
    def __init__(self, app, client, ip, method, path, query, headers, content):
        """
            An object representing an HTTP request serviced by dhttp.
        
        Arguments:
            app {DHTTPServer} -- The app coordinating the servicing of this request.
            client {dhttp.tcp.AsyncTCPServer.Client} -- The client originating the request.
            ip {str} -- The IP the request came from.
            method {str} -- The method of the request, e.g. 'GET' or 'POST'.
            path {str} -- The path of the request, e.g. '/index.html'.
            query {List[Tuple[str, str]]} -- The query contents of the path, e.g. [('myname', 'JohnDoe'), ('spaces', 'false')]
            headers {Dict[str, str]} -- The headers of the HTTP request.
            content {bytes} -- The body, in bytes, of the HTTP request.
        """
        self.method = method
        self.headers = headers
        self.content = content
        self.ip = ip
        self.app = app
        self.client = client
        self.path = path
        self.query = query
        self.query_dict = {a: b for i, (a, b) in enumerate(query) if [x[0] for x in query].index(a) == i}

    def resolve_path(self):
        path = self.path

        while path in self.app.aliases:
            path = self.app.aliases[path]

        return path

    def get_log(self) -> DHTTPRequestLog:
        return DHTTPRequestLog(self.method, self.ip, self.path, self)

    def get_header(self, name):
        """
            Grabs a header from the request, by name.
        Ignores case.
        
        Arguments:
            name {str} -- The header's name.
        
        Returns:
            str -- The header's content.
        """
        return self.headers.get(name.upper(), '')

class DHTTPResponse(object):
    """
        A DHTTP response 'accumulation' object,  used to write to
    the response's body and set headers before sending the actual
    response back.
    """
    

    def __init__(self, app, request, headers, write):
        self.app = app
        self.headers = headers
        self.request = request
        self.__write = write
        self.content = tcpserver.DequeBytesIO()
        self._status = None

        self._on_close = set()
        self._on_error = set()
        self.closed = False

        self._properties = {}

    def _write(self, data):
        self.catch_error(self.__write)(data)

    def status(self, status):
        """
            Sets the HTTP status of this response, as a string defined
        as '<status number> <status code>'>

            For example:

                res.status('404 NOT FOUND')
                res.end('Look again, pal!')
        
        Arguments:
            status {str} -- The status string.
        """
        self._status = status

    def on_error(self, func):
        self._on_error.add(func)
        return func

    def on_close(self, func):
        self._on_close.add(func)
        return func

    def __setitem__(self, key, value):
        self._properties[key] = value

    def __getitem__(self, key):
        return self._properties[key]

    def set(self, name, value):
        """
            Sets a response header.
        
        Arguments:
            name {str} -- The name of the header.
            value {str} -- The value of the header.
        """
        self.headers[name] = value

    def write(self, string):
        """
            Write data into the response body.
        
        Arguments:
            string {str|bytes} -- Data to be written.
        
        Raises:
            BaseException --        Raised if  the response itself was
                                already sent over when data is written
                                to the accumulator's content buffer.
        """


        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        if isinstance(string, bytes):
            self.content.write(string)

        else:
            self.content.write(string.encode('utf-8'))

    def _error(self):
        if not self.closed:
            self.status('500 INTERNAL SERVER ERROR')
            self.end()

    def close(self):
        for f in self._on_close | self.app._on_resp_close:
            self.catch_error(f)(self.request, self)

        self.closed = True

    def catch_error(self, func):
        def __inner__(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except (BrokenPipeError, ConnectionResetError):
                pass

            except BaseException as err:
                call_str = func.__name__ + '('
                call_str += ', '.join(type(x).__name__ for x in args)

                if len(kwargs) > 0:
                    call_str += ', ' + ', '.join(f'{x[0]} = {type(x[1]).__name__}' for x in kwargs.items())

                call_str += ')'

                for f in self._on_error | self.app._on_error:
                    try:
                        f((func, args, kwargs, call_str), err)

                    except BaseException:
                        traceback.print_exc()
                        continue

                return None

        return __inner__

    def end(self, end_data = ''):
        """
            Closes this request, optionally writing
        the given data to  the content accumulation
        buffer first.   End data is appended to the
        body of the actual respnse.
        
        Keyword Arguments:
            end_data {str} --       Data appended to the
                                response body.
                                (default: {''})
        
        Raises:
            BaseException --        Raised if the response was already
                                ended, sent and closed.
        """

        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        self.write(end_data)
        self.close()

        size_length = len(self.content)
        self.headers['Content-Length'] = size_length

        # finish up and send response headers
        if self._status is None:
            self._write(b'HTTP/1.1 200 OK\r\n')

        else:
            self._write(f'HTTP/1.1 {self._status}\r\n'.encode('utf-8'))

        h = hashlib.md5()
        h.update(self.content.read_all())
        self.headers.setdefault('Content-MD5', base64.b64encode(h.digest()).decode('utf-8'))
        self.headers.setdefault('Content-Type', 'text/html; encoding=utf-8')

        for name, value in self.headers.items():
            self._write('{name}: {value}\r\n'.format(name = name, value = str(value).strip('\r\n')).encode('utf-8'))

        # send response content
        self._write(b'\r\n')
        self._write(self.content.read_all())

class HTTPHandler(object):
    def __init__(self, dhttp):
        self.dhttp = dhttp

        self.dhttp_reset()

    def dhttp_reset(self, write = None, status_data = None):
        if status_data is not None:
            write(status_data)

        self.method = None
        self.path = None
        self.headers = {}
        self.content = tcpserver.DequeBytesIO()
        self.state = "BEGIN"
        self._line = b''
        self.line_buffering = True

    async def _recv(self, data, writer, client):
        if client in self.dhttp._ignore_http:
            return

        if self.line_buffering:
            self._line += data
                
            lines = self._line.split(b'\n')
            self._line = lines[-1]
            lines = lines[:-1]

            while len(lines) > 0:
                await self.handle(lines[0].strip(b'\r'), writer, client)
                lines = lines[1:]

                if not self.line_buffering:
                    data = b'\n'.join(lines) + self._line
                    self._line = b''
                    await self.handle(data, writer, client)
                    break
            
        else:
            await self.handle(data, writer)

    def finish(self):
        self.dhttp_reset()

    async def handle(self, data, writer, client):
        if self.state == 'BEGIN':
            try:
                start_line = data.decode('utf-8')

            except UnicodeDecodeError as err:
                self.dhttp_reset(writer, b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                return

            if start_line == '':
                return

            start_line = start_line.split(' ')

            # B: make sure it has 3 space-separated parts

            if len(start_line) != 3:
                self.dhttp_reset(writer, b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')

            else:
                (self.method, path, version) = start_line

                self.path = path.split('?')[0]
                self.query = urllib.parse.parse_qsl(path.split('?')[-1])

                # C: ensure parseable version
                match = re.match(r'^([A-Z]+)/(\d+)\.(\d+)$', version)

                if match is None:
                    self.dhttp_reset(writer, b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')

                else:
                    # D: ensure version is HTTP/1.0
                    (protocol, major, minor) = match.groups()

                    if protocol != 'HTTP' or major != '1':
                        self.dhttp_reset(writer, b'HTTP/1.1 505 HTTP VERSION NOT SUPPORTED\r\n\r\n')

                    else:
                        self.state = 'HEADERS'

        elif self.state == 'HEADERS':
            try:
                header_line = data.decode('utf-8')

            except UnicodeDecodeError:
                self.dhttp_reset(writer, b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                return

            # E: check if empty line (header-terminating CRLF)
            if len(header_line) == 0:
                # F: check if the 'Content-Length' header is not null
                try:
                    if int(self.headers.get('CONTENT-LENGTH', 0)) <= 0:
                        await self.handle_http_request(writer, client)
                        self.state = 'BEGIN'

                    else:
                        self._content_length = int(self.headers['CONTENT-LENGTH'])
                        self.line_buffering = False
                        self.state = 'CONTENT'

                except ValueError:
                    self.dhttp_reset(writer, b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                    self.state = 'BEGIN'
                    return

            else:
                match = re.match(r'^([^\s:]+): (.+)$', header_line)

                # G: check if header matches format
                if match is None:
                    self.dhttp_reset(writer, b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                    self.finish()
                    return

                else:
                    (name, value) = match.groups()
                    self.headers[name.upper()] = value

        elif self.state == 'CONTENT':
            self.content.write(data)

            if len(self.content) >= self._content_length:
                await self.handle_http_request(writer, client)
                self.line_buffering = True

                tail = self.content.slice(self._content_length)

                if tail is not None:
                    self._recv(tail)

                self.finish()
                return

    async def receive(self, data, write, client):
        self.client_address = client.address
        await self._recv(data, write, client)

    async def handle_http_request(self, write, client):
        self.content.seek(0)
        await self.dhttp._receive_request(DHTTPRequest(self.dhttp, client, self.client_address[0], self.method, self.path, self.query, self.headers, self.content.read()), write)

class DHTTPServer(object):
    """
        A DHTTP server application. Similar to
    Node.js's express(),   you can use this to
    serve  a multitude of  different kinds  of
    documents, media and multimedia via simple
    HTTP.
    """

    def __init__(self):
        self.paths = {}
        self.aliases = {}

        self.event_log = []
        self.middleware = []
        self.log_handlers = set()

        self.handler = HTTPHandler(self)
        self._on_error = set()
        self._on_resp_close = set()
        self._on_service_error = set()

        self.tcp_servers = []
        self._ignore_http = set()
        self.ticking = False
        
    def remove_port(self, port):
        """
        Removes a listen port.
        """

        self.tcp_servers = [x for x in self.tcp_servers if x[0] != port]

    def add_port(self, port, *args, **kwargs):
        """
        Adds a port to listen to. Accepts extra
        arguments, which will be passed to the
        corresponding AsyncTCPServer's run
        method once this DHTTP server is run.
        
        Arguments:
            port {int} -- The corresponding AsyncTCPServer's listen port.
        """

        if port in (x[0] for x in self.tcp_servers):
            raise ValueError('This port is already taken!')

        serv = tcpserver.AsyncTCPServer()

        @serv.receiver
        async def _receiver(client, data):
            await self.handler.receive(data, client.write, client)

        self.tcp_servers.append((port, serv, args, kwargs))

    def on_response_finish(self, func):
        """
            Decorator to be  used  to call
        back  everytime any  DHTTPResponse
        from this server has finished.
        
        Arguments:
            func {Function} --      A callback, i.e.
                                the decorated function.
        """
        self._on_resp_close.add(func)

    def on_service_error(self, func):
        """
            Decorator to be  used  to  handle
        an error emerging from  your own HTTP
        handling callbacks,   i.e. those that
        were registered via app.get, app.post
        or app.put (generalizing, app.on).
        
        Arguments:
            func {Function} --      A callback, i.e.
                                the decorated function.
        """
        self._on_service_error.add(func)
        return func

    def on_response_error(self, func):
        """
            Decorator  to be  used  to  handle
        an error emerging from a DHTTPResponse
        object (i.e. a 'res').
        
        Arguments:
            func {Function} --      A callback, i.e.
                                the decorated function.
        """
        self._on_error.add(func)
        return func

    def run_forever(self):
        """
            Handles HTTP requests until the stop method is called explicitly.
        Internally calls trio.run(). Accepts extra tcpserver.AsyncTCPServer.run
        arguments.
        """
        
        def _decorator(cb = None):
            try:
                self.ticking = True

                if cb is not None:
                    cb()
                    
                trio.run(self.run)

            except KeyboardInterrupt:
                self.stop()

        return _decorator

    def stop(self):
        for _, s, _, _ in self.tcp_servers:
            s.stop()

    async def run(self):
        """
            Handles HTTP requests until the stop method is called explicitly.
        Uses trio. Accepts extra tcpserver arguments.
        """
        self.ticking = True

        async with trio.open_nursery() as nursery:
            for port, s, args, kwargs in self.tcp_servers:
                nursery.start_soon(functools.partial(s.run, port, *args, **kwargs))

        self.ticking = False

    def start(self, *_):
        """
            Does nothing; left for compatibiltiy purposes.
        """
        pass

    def handle_once(self):
        raise NotImplementedError("Handling one request at a time was removed, as `socketserver` was abandoned.")

    def on_log(self, func):
        """
            Adds a log handler, called everytime a request is
        to be logged.   One  may  also  use  a  middleware if
        preferred.
        
        Arguments:
            func {Function} --      This function is a decorator,
                                thus it takes a    function as an
                                argument. Use it like this:

                                    @app.on_log
                                    def logger(dhlog):
                                        print("> " + str(dhlog))
        """
        self.log_handlers.add(func)
        return func

    async def _receive_request(self, req, write):
        try:
            log = req.get_log()
            self.event_log.append(log)

            for log_handler in self.log_handlers:
                log_handler(log)

            path = req.resolve_path()
                
            headers = {}

            if req.method in self.paths:
                for (cbpath, request_handler) in self.paths[req.method]:
                    if fnmatch.fnmatch(path, cbpath):
                        for header in request_handler.headers:
                            headers[header[0]] = headers[1]

            res = DHTTPResponse(self, req, headers, write)

            for (mpath, mw) in self.middleware:
                if mpath is None or mpath == path:
                    flag = mw(req, res)

                    if flag is None:
                        continue

                    elif flag == 'STOP':
                        if res.closed:
                            return

                        else:
                            break

                    elif flag == 'BREAK':
                        break

                    else:
                        print(DHTTPGenericLog('WARN', f'Unknown middleware return flag: {repr(flag)}\n    Expected either of: nothing/None (to continue), STOP, BREAK.\n    Ignoring and continuing...'))
                        continue

            found = False

            if req.method in self.paths:
                async with trio.open_nursery() as nursery:
                    for (cbpath, request_handler) in self.paths[req.method]:
                        if fnmatch.fnmatch(path, cbpath):
                            found = True

                            try:
                                if inspect.iscoroutinefunction(request_handler.callback):
                                    nursery.start_soon(request_handler.callback, req, res)

                                else:
                                    request_handler.callback(req, res)

                                if res.closed:
                                    break

                            except BaseException as e:
                                traceback.print_exc()
                                send_500 = True

                                for e in self._on_service_error:
                                    send_500 = send_500 and not bool(e(req, res))

                                if send_500:
                                    res._error()

            if not found or not res.closed:
                res.status('404 NOT FOUND')
                res.end()

        except (BrokenPipeError, ConnectionResetError):
            return

    def remove(self, method):
        """
            Removes all HTTP request handlers whose callback
        is the given function argument.
        
        Arguments:
            method {Function} -- The callback to remove.
        
        Returns:
            set --        All handlers found that contained  this
                      callback  that  were  removed.   Since  the
                      callback part of the handlers is always the
                      same, the list contains  only  the paths of
                      such handlers.
        """
        removed = set()

        for key, callbacks in self.paths.items():
            self.paths[key] = [(i, m) for (i, m) in callbacks if m is not method]
            found = set(i for (i, m) in callbacks if m is method)
            removed |= found

        return removed

    def on(self, method, path, headers = ()):
        """
            Generic HTTP request handler decorator. Use
        only if   you want to listen to  a non-standard
        (i.e.   other than GET, POST or  PUT)   request
        method.
        
        Arguments:
            method {str} --         The HTTP method to listen to
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            function --             The inner decorator function. Returning
                                another decorator   instead of   the  inner
                                function   directly   is a   way to  supply
                                arguments  to the  actual  inner  function,
                                like so:

                                    def decor1(func_arg):
                                        def decor2(callback):
                                            def __inner__(*args):
                                                return func_arg(*[callback(a) for a in args])

                                            return __inner__

                                        return __decor2__

                                    def sum(a, b):
                                        print(a + b)

                                    @decor1(sum)
                                    def double_sum(a):
                                        return a * 2

                                    double_sum(3, 4) # returns 14 (2*3 + 2*4 = 2(3 + 4) = 2*7 = 14)
        """

        if isinstance(headers, dict):
            headers = headers.items()

        def _decorator(callback):
            self.paths.setdefault(method, []).append((path, DHTTPCallback(headers, callback)))
            return callback

        return _decorator

    def use(self, path = None):
        """
            The standard middleware handler decorator.

            Use to handle every (or a specific kind of) HTTP
        request (with a corresponding response object,  i.e.
        res), before it is even processed by  an actual GET,
        POST or PUT handler.  Useful for things like loggers
        and modifiers. Inspired by Express.

            For example:

                @app.use()
                def set_time(req, res):
                    res['time'] = datetime.datetime.utcnow().strftime('%H:%M:%S')

                SIMULATE_POST = True

                @app.use('/api/*')
                def api_filter(req, res):
                    if req.method == 'GET':
                        if SIMULATE_POST:
                            req.method = 'POST'

                        else:
                            res.status('400 BAD REQUEST')
                            res.end('The API can only be accessed via POST methods! :/')

            Keep in mind that a response object can keep any
        kind of property as a dict:

                res['my_prop'] = 5
                res['data'] = {"John Doe": req.content.read().decode('utf-8')}
        
        Keyword Arguments:
            path {str} -- An fnmatch mask of all HTTP paths to preprocess.
                          (default: {None} -- Preprocess everything!)
        """
        def _decorator(callback):
            self.middleware.append((path, callback))
            return callback

        return _decorator

    def unuse(self, func):
        """
            Removes a middleware callback, by removing every
        request preprocessing handler whose callback  is the
        func, a la 'func1 is func2'.
        
        Arguments:
            func {Function} -- The middleware handler to remove.
        """
        new_mw = []

        for (i, middle) in enumerate(self.middleware):
            if middle[1] is not func:
                new_mw.append(middle)

        self.middleware = new_mw

    def get(self, path, headers = ()):
        """
            Decorated functions serve any GET requests whose
        path matches the fnmatch mask argument 'path'.

            For example:
                
                @app.get('/time')
                def http__utc_time(req, res):
                    res.end("Right now in the UTC it is {}. Thank you.".format(
                        datetime.datetime.utcnow().strftime('%H:%M:%S')
                    ))

            The function can still be supplied as an argument
        to the 'remove' method, to disable it:

                app.remove(http__utc_time)
        
        Arguments:
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --   What Python sees as the actual decorator.
        """

        def _decorator(callback):
            self.on('GET', path, headers)(callback)
            return callback

        return _decorator

    def post(self, path, headers = ()):
        """
            Decorated functions serve any POST requests whose
        path matches the fnmatch mask argument 'path'.

            For example:
                
                import time

                @app.post('/unixtime')
                def http__unix_time(req, res):
                    res.end(time.time())

            The function can still be supplied as an argument
        to the 'remove' method, to disable it:

                app.remove(http__unix_time)
        
        Arguments:
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --   What Python sees as the actual decorator.
        """

        def _decorator(callback):
            self.on('POST', path, headers)(callback)
            return callback

        return _decorator

    
    def websocket(self, path, allowed_hosts = None):
        def _decorator(func):
            @self.get(path)
            async def _handler(req, res):
                def fail():
                    """
                    Fail the WebSocket connection.
                    """
                    pass

                if (
                    req.get_header('Connection') and req.get_header('Upgrade') and

                    'UPGRADE' in req.get_header('Connection').upper().split(', ') and
                    req.get_header('Upgrade').upper() == 'WEBSOCKET'
                ):
                    # verify Sec-WebSocket-Key
                    swsk = req.get_header('Sec-WebSocket-Key')

                    if swsk == '':
                        return fail()

                    try:
                        ws_key = base64.b64decode(swsk)

                    except binascii.Error:
                        return fail()

                    if len(ws_key) != 16:
                        return fail()

                    # verify Sec-WebSocket-Version
                    if req.get_header('Sec-WebSocket-Version') != '13':
                        return fail()

                    # verify host header
                    nice_host = False

                    if allowed_hosts is None:
                        nice_host = True

                    elif (
                        req.get_header('Host') in (x + str(p) for x in ('127.0.0.1:{port}', 'localhost:{port}') for (p, _, _, _) in self.tcp_servers) and
                        req.client.address[0] in ('localhost', '127.0.0.1')
                    ):
                        nice_host = True

                    else:
                        for h in allowed_hosts:
                            if fnmatch.fnamtch(req.get_header('Host'), h):
                                nice_host = True

                    if not nice_host:
                        return fail()

                    # Wrap and fix the client for WebSocket
                    client = req.client
                    self._ignore_http.add(client)
                    wrap_websocket(client, self, False)

                    # End the HTTP response
                    res.status('101 SWITCHING PROTOCOLS')
                    res.set('Upgrade', 'websocket')
                    res.set('Connection', 'upgrade')

                    acc = hashlib.sha1(swsk.encode('utf-8') + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
                    data = base64.b64encode(acc.digest())
                    res.set('Sec-WebSocket-Accept', data.decode('utf-8'))
                    res.end()

                    if req.get_header('Sec-WebSocket-Protocol') != '':
                        res.set('Sec-WebSocket-Protocol', req.get('Sec-WebSocket-Protocol'))

                    if inspect.iscoroutinefunction(func):
                        await func(client, req)

                    else:
                        func(client, req)

                return 'DONE'

            return _handler
        
        return _decorator

    def put(self, path, headers = ()):
        """
            Decorated functions serve any POST requests whose
        path matches the fnmatch mask argument 'path'.

            For example:

                id = 0

                @app.put('/giveimage')
                def http__put_image(req, res):
                    image_id = id
                    id += 1

                    #   NEVER FORGET YOUR SECURITY AND SANITY CHECKS!!
                    # Don't write to your filesystem random files that
                    # people give you. This is a MERE ILLUSTRATIVE
                    # EXAMPLE.
                    open('{}.png'.format(image_id), 'wb').write(req.content)

                    res.end(str(image_id))

            The function can still be supplied as an argument
        to the 'remove' method, to disable it:

                app.remove(http__put_image)
        
        Arguments:
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --   What Python sees as the actual decorator.
        """

        def _decorator(callback):
            self.on('PUT', path, headers)(callback)
            return callback

        return _decorator

    def serve(self, path, filename, headers = ()):
        """
            Serves a single file as a GET request
        handler, e.g. for download.

            http__boring_document = app.serve('/serious_business.pdf', 'I_hope_my_boss_doesn't_see_this_filename.pdf')
        
        Arguments:
            path {str} -- The HTTP path at the which to serve this file.
            filename {[type]} -- The path to the file to serve.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --         The actual callback, which internally
                            is itself decorated via the 'get' method.
                            Thus,   you can use  the return value  to
                            remove a 'serve' handler:

                                app.remove(http__boring_document)
        """

        @self.get(path, headers)
        def _callback(req: DHTTPRequest, res: DHTTPResponse):
            if os.path.isfile(filename):
                res.set('Content-Type', mimetypes.guess_type(filename)[0])

                with open(filename, 'rb') as fp:
                    res.end(fp.read())

        return _callback

    def jinja(self, path, template, headers = (), method = 'GET'):
        _temp = template
        """
            Serves a single Jinja template as a string
        or Template object,  which will be rendered to
        create a single, dynamic HTML page,  using the
        parameters returned by the decorated callback.

            A decorated function is used to be able to determine
        the Jinja template parameters, although a static dict or
        dict-like iterable can also be used instead.   Arguments
        to the decorated function are:

                --      `req`, to know the content of the served
                    request;

                --      A 'set' callback, which sets a parameter
                    used when rendering the template;

                --      A 'done' function, which serves the page
                    when called. It can be called with  a status
                    value,     like  '404  NOT  FOUND'  or  '403
                    FORBIDDEN',    though it will    (of course)
                    default to 200.
        
        For example,

            @app.jinja('/cgi/time', '{{ utctime }}')
            def cgi_time_str(req, res, set, done):
                set('utcftime', datetime.datetime.utcnow().strftime('%H:%M:%S'))
                done()
        
        Arguments:
            path {str} --                                       The root HTTP path at the which  to serve the pages.

            template {str|jinja2.Template} --                   The Jinja template as a string or Template object.
        
        Keyword Arguments:
                                                    
            headers {list} --                           A  list  of  default  response  headers.   Will   be
                                                    overriden if res.set is called.
                                                    (default: {[]})

            method  {str}  --                           The request method to serve.
                                                    (default: 'GET')

        Returns:
                The decorator. Decorated functions become a
            DHTTP handler, which can be then remove()'d.
        """
        def _decorator(param_callback):
            """
            The actual decorator returned by the function.
            

            Arguments:
                param_callback {[type]} -- used to be able to 
        determine the Jinja template parameters,   although a 
        static dict  or  dict-like iterable can  also be used 
        instead.   Arguments to the function are:

                --      A 'req' (DHTTPRequest),    to know the
                    served request;

                --      A 'set' callback, which sets a parameter
                    used when rendering the template;

                --      A 'done' function, which serves the page
                    when called. It can be called with  a status
                    value,     like  '404  NOT  FOUND'  or  '403
                    FORBIDDEN',    though it will    (of course)
                    default to 200.
            
            Returns:
                The DHTTP handler, which can be then remove()'d.
            """
            template = _temp
            is_callback = hasattr(param_callback, '__call__')

            if isinstance(template, str):
                template = jinja2.Template(template)

            @self.on(method, path, headers)
            async def _callback(req, res):
                params = {}

                if is_callback:
                    def set_param(key, val):
                        params[key] = val

                    def done(status = None):
                        if status is not None:
                            res.status(status)

                        if not res.closed:
                            res.end(template.render(**params))

                    if inspect.iscoroutinefunction(param_callback):
                        await param_callback(req, set_param, done)

                    else:
                        param_callback(req, set_param, done)

                else:
                    res.end(template.render(**dict(param_callback)))

            return _callback

        return _decorator

    def jinja_folder(self, path, folder_path, headers = (), method = 'GET'):
        """
            Serves a folder containing Jinja templates,
        which will  be rendered  to create  web  pages,
        with the parameters returned   by the decorated
        callback.

            A decorated function is used to be able to determine
        the Jinja template parameters, although a static dict or
        dict-like iterable can also be used instead.   Arguments
        to the decorated function are:

                --      `req`, to know the content of the served
                    request;

                --      A 'set' callback, which sets a parameter
                    used when rendering the template;

                --      A 'done' function, which serves the page
                    when called. It can be called with  a status
                    value,     like  '404  NOT  FOUND'  or  '403
                    FORBIDDEN',    though it will    (of course)
                    default to 200.
        
        For example,

            @app.jinja_folder('/cgi', './templates')
            def cgi_parameters(req, res, set, done):
                set('time', time.time())
                set('utcftime', datetime.datetime.utcnow().strftime('%H:%M:%S'))
                done()
        
        Arguments:
            path {str} --                               The root HTTP path at the which  to serve the pages.

            folder_path {str} --                        The path of the folder to be server.
        
        Keyword Arguments:
                                                    
            headers {list} --                           A  list  of  default  response  headers.   Will   be
                                                    overriden if res.set is called.
                                                    (default: {[]})

            method  {str}  --                           The request method to serve.
                                                    (default: 'GET')

        Returns:
                The decorator. Decorated functions become a
            DHTTP handler, which can be then remove()'d.
        """
        def _decorator(param_callback):
            """
            The actual decorator returned by the function.
            

            Arguments:
                param_callback {[type]} -- used to be able to 
        determine the Jinja template parameters,   although a 
        static dict  or  dict-like iterable can  also be used 
        instead.   Arguments to the function are:

                --      A 'req' (DHTTPRequest),    to know the
                    served request;

                --      A 'set' callback, which sets a parameter
                    used when rendering the template;

                --      A 'done' function, which serves the page
                    when called. It can be called with  a status
                    value,     like  '404  NOT  FOUND'  or  '403
                    FORBIDDEN',    though it will    (of course)
                    default to 200.
            
            Returns:
                The DHTTP handler, which can be then remove()'d.
            """
            is_callback = hasattr(param_callback, '__call__')
            env = jinja2.Environment(
                loader = jinja2.FileSystemLoader(os.path.join('.', folder_path)),
                autoescape = jinja2.select_autoescape(['html', 'xml'])
            )

            @self.on(method, os.path.join(path, '*'), headers)
            async def _callback(req, res):
                fpath = os.path.join(folder_path, os.path.relpath(req.path, path))

                if os.path.isfile(fpath):
                    try:
                        template = env.get_template(os.path.relpath(req.path, path))

                    except (jinja2.TemplateError, jinja2.UndefinedError):
                        traceback.print_exc()
                        res.status('500 INTERNAL SERVER ERROR')
                        res.end()
                        return

                    params = {}

                    res.set('Content-Type', mimetypes.guess_type(fpath)[0])

                    if is_callback:
                        def set_param(key, val):
                            params[key] = val

                        def done(status = None):
                            if status is not None:
                                res.status(status)

                            if not res.closed:
                                res.end(template.render(**params))

                        if inspect.iscoroutinefunction(param_callback):
                            await param_callback(req, set_param, done)

                        else:
                            param_callback(req, set_param, done)

                    else:
                        res.end(template.render(**dict(param_callback)))

            return _callback

        return _decorator

    def static(self, path, folder_path, headers = ()):
        """
            Serves a folder as a single,  masked GET request
        handler, e.g. to host a bunch of CSS and JS files at
        once.

            http__pictures_folder = app.static('/pics', './pictures')
        
        Arguments:
            path {str} -- The root HTTP path at the which to serve this folder.
            folder_path {[type]} -- The path of the folder to be served.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --         The actual callback, which internally
                            is itself decorated via the 'get' method.
                            Thus,   you can use  the return value  to
                            remove a 'serve' handler:

                                app.remove(http__pictures_folder)
        """

        @self.get(os.path.join(path, '*'), headers)
        def _callback(req, res):
            fpath = os.path.join(folder_path, os.path.relpath(req.path, path))

            if os.path.isfile(fpath):
                res.set('Content-Type', mimetypes.guess_type(fpath)[0])

                with open(fpath, 'rb') as fp:
                    res.end(fp.read())

        return _callback

    def alias(self, path, new_path):
        """
            Aliases an HTTP path to another one, so you can
        visit the same document via both paths,   or merely
        replace an existing path by  aliasing it to another
        one.
        
        Arguments:
            path {str} --     The path to alias.
            new_path {str} -- The path to be aliased to.
        """
        self.aliases[path] = new_path


class DHTTPClientResponse(object):
    def __init__(self, status, headers, content):
        self.status = status
        self.headers = headers
        self.content = content

    def has(self,header_name):
        return header_name.upper() in self.headers

    def get(self, header_name):
        """
        Gets a header from the HTTP response.
        
        Arguments:
            header_name {str} -- Case-insensitive header name.
        
        Returns:
            str -- Data in the header.
        """

        return self.headers.get(header_name.upper(), '')

    def status_number(self):
        """
        Gets the status number of this HTTP response.
        
        Returns:
            int -- The status number! It is definitely not a complex number. :D
        """

        return int(self.status.split(' ')[0])


class DHTTPClientResponseReader(object):
    def __init__(self, tcp_client):
        self._on_response = set()
        self.client = tcp_client
        self.reset()

        self.client.receiver(self._recv)

    def reset(self):
        self.status = None
        self.headers = {}
        self.content = tcp.DequeBytesIO()

        self.state = "BEGIN"
        self._line = b''
        self.line_buffering = True

    def on_response(self, f):
        """
        Registers a function to be used as a handler
        called everytime an HTTP response is retrieved.

        Can be used as a decorator. f can be async.
        """

        self._on_response.add(f)
        return f

    async def _recv(self, data):
        try:
            if self.line_buffering:
                self._line += data
                    
                lines = self._line.split(b'\n')
                self._line = lines[-1]
                lines = lines[:-1]

                while len(lines) > 0:
                    try:
                        await self.handle(lines[0].strip(b'\r').decode('utf-8'))

                    except UnicodeDecodeError:
                        self.client.write(b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                        self.reset()
                        return

                    lines = lines[1:]

                    if not self.line_buffering:
                        data = b'\n'.join(lines) + self._line
                        self._line = b''
                        await self.handle(data)
                        break
                
            else:
                await self.handle(data)

        except (BaseException, UnicodeError) as err:
            traceback.print_exc()

    async def handle(self, data):
        if self.state == 'BEGIN':
            status_line = re.match(r'^HTTP/([^ ]+) (.+)$', data)

            if status_line is not None:
                (ver, status) = status_line.groups()

                if ver != '1.1':
                    warnings.warn(ValueError(f'Unsupported HTTP version: {repr(ver)}'))

                else:
                    self.status = status
                    self.state = 'HEADERS'

            else:
                warnings.warn(ValueError(f'Invalid HTTP response status line: {repr(data)}'))
                self.reset()

        elif self.state == 'HEADERS':
            if len(data) == 0:
                try:
                    if int(self.headers.get('CONTENT-LENGTH', 0)) <= 0:
                        await self.got_response()
                        self.reset()

                    else:
                        self._content_length = int(self.headers['CONTENT-LENGTH'])
                        self.line_buffering = False
                        self.state = 'CONTENT'

                except ValueError:
                    if 'CONTENT-LENGTH' in self.headers:
                        warnings.warn(ValueError(f'Invalid HTTP Content-Length value: {repr(self.headers["CONTENT-LENGTH"])}'))
                        self.reset()
                        return

                    else:
                        raise

            else:
                match = re.match(r'^([^\s:]+): (.+)$', data)

                # G: check if header matches format
                if match is None:
                    warnings.warn(ValueError(f"Invalid HTTP header line: {repr(data)} - ignoring."))
                    return

                else:
                    (name, value) = match.groups()
                    self.headers[name.upper()] = value
            
        elif self.state == 'CONTENT':
            self.content.write(data)

            if len(self.content) >= self._content_length:
                await self.got_response()
                self.line_buffering = True

                tail = self.content.slice(self._content_length)

                if tail is not None:
                    self._recv(tail)

                self.reset()
                return

    async def got_response(self):
        resp = DHTTPClientResponse(self.status, self.headers, self.content)

        async def sync_handler(f):
            f(resp)

        async with trio.open_nursery() as nursery:
            for f in self._on_response:
                if inspect.iscoroutinefunction(f):
                    nursery.start_soon(f, resp)

                else:
                    nursery.start_soon(sync_handler, f)


class DHTTPClient(object):
    """
    A connection, as a client, to a HTTP server, the latter
    which, by the way, doesn't need to be a dhttp server.

    Arguments:
        host {str} -- The hostname of the server to connect to.

    Keyword Arguments:
        port {int} -- The port of the server to connect to. (default: {80})
    """

    def __init__(self, host, port = 80):
        self.host = host
        self.port = port

        self.client = tcp.AsyncTCPClient()
        self.running = False
        self.connected = False
        self.response_reader = DHTTPClientResponseReader(self.client)

        self._on_response = set()
        self._resp = None

        self.response_reader.on_response(self.got_response)

    def reset_response_handlers(self):
        """
        Resets this connection's response handler register.
        """

        self._on_response = set()

    def on_response(self, f):
        """
        Registers a function to be used as a handler
        called everytime an HTTP response is retrieved.

        Can be used as a decorator. f can be async.
        """

        if self.connected == 2:
            f(self._resp)

        self._on_response.add(f)
        return f

    async def start(self, *args, **kwargs):
        if not self.running:
            self.running = True

            if self.client.connected:
                await self.client.run()

            else:
                await self.client.run_connect(self.host, self.port, *args, **kwargs)

    def stop(self):
        if self.running:
            self.running = False
            self.client.stop()

    async def request(self, path = '/', method = 'GET', headers = (), data = b'', tls = False, cert_mode = tcpserver.CertMode.CM_GENERATED, fn_component = '', cert_file = None, key_file = None, key_size = 2048):
        if fn_component:
            if key_file is None:
                key_file = ".{}.key.pem".format(fn_component)

            if cert_file is None:
                cert_file = ".{}.cert.pem".format(fn_component)

        if not self.client.connected:
            await self.client.connect(self.host, self.port, tls = tls, cert_mode = cert_mode, cert_file = cert_file, key_file = key_file, key_size = key_size)

        headers = dict(headers)
        
        host = f"{self.host}{'' if self.port == 80 else ':' + str(self.port)}"
        origin = f"http://{self.host}:{self.port}"

        if isinstance(data, str):
            data = data.encode('utf-8')

        elif isinstance(data, bytearray):
            data = bytes(data)

        elif not isinstance(data, bytes):
            raise ValueError("data must be a bytes or bytes-like object!")

        h = hashlib.md5(data)

        if data:
            headers.setdefault('Content-Length', len(data))
            headers.setdefault('Content-MD5', base64.b64encode(h.digest()).decode('utf-8'))

        headers.setdefault('Host', host)
        headers.setdefault('Origin', origin)

        self.client.write(f'{method} {path.strip(" ")} HTTP/1.1\r\n'.encode('utf-8'))

        for name, value in headers.items():
            self.client.write('{name}: {value}\r\n'.format(name = name, value = str(value).strip('\r\n')).encode('utf-8'))

        self.client.write(b'\r\n' + data)

    async def got_response(self, resp):
        self._resp = resp

        async def sync_handler(f):
            f(resp)

        async with trio.open_nursery() as nursery:
            for f in self._on_response:
                if inspect.iscoroutinefunction(f):
                    nursery.start_soon(f, resp)

                else:
                    nursery.start_soon(sync_handler, f)


class BaseDHTTPException(BaseException):
    pass

class BaseDHTTPNetworkException(BaseDHTTPException):
    pass

class HandshakeError(BaseDHTTPNetworkException):
    pass

class HTTPStatusError(BaseDHTTPNetworkException):
    pass

class WSHandshakeError(HandshakeError):
    pass


class DHTTPWebsocketClient(object):
    def __init__(self, host, port = 80):
        self.host = host
        self.port = port
        self.path = None

        self.conn = DHTTPClient(host, port)
        self.conn.on_response(self.handle_response)
        self.conn.client.on_close(self._on_close)

        self._on_connect = set()

        self.running = False
        self.connected = False

        self.ws_key = None
        self.ws_accept = None
        self.ws_subprotocol = None

        self._resp = None


    def _on_close(self):
        self.running = False
        self.connected = False

        self.ws_key = None
        self.ws_accept = None
        self.ws_subprotocol = None

        self._resp = None


    def on_connect(self, f):
        """
        Registers a handler to be called once the
        WebSocket is connected. f may be async.
        This method may be used as a decorator.
        
        Arguments:
            f {funtion} -- The handler.
        """

        if self.connected == 2:
            f(self._resp)

        self._on_connect.add(f)
        return f

    async def handle_response(self, resp: DHTTPClientResponse):
        """
        Internal function, do not call.

        Arguments:
            resp {DHTTPClientResponse} -- The response to handle.
        """

        if resp.status_number() != 101:
            raise HTTPStatusError('Got a bad or invalid HTTP status while trying to upgrade to a WebSocket connection:  ' + resp.status)

        elif not resp.has('Upgrade') or resp.get('Upgrade').upper() != 'WEBSOCKET':
            raise HTTPStatusError('Got no HTTP upgrade, or an invalid one, instead of a WebSocket upgrade:  ' + ('(none)' if not resp.has('Upgrade') else repr(resp.get('Upgrade'))))

        elif not resp.has('Sec-WebSocket-Accept'):
            raise WSHandshakeError('Sec-WebSocket-Accept not found in the response!')

        else:
            try:
                acc = base64.b64decode(resp.get('Sec-WebSocket-Accept'))

            except binascii.Error:
                raise WSHandshakeError(f'Sec-WebSocket-Accept header in the response is not a valid Base64 value!')

            else:
                if acc != self.ws_accept:
                    raise WSHandshakeError(f'The response\'s Sec-WebSocket-Accept header value does not match the predicted key (expected {base64.b64encode(self.ws_accept)}, got {base64.b64encode(acc)})!')

                elif resp.has('Sec-WebSocket-Extensions'):
                    raise WSHandshakeError('Sec-WebSocket-Extensions is not supported!')

                elif resp.has('Sec-WebSocket-Protocol') != bool(self.ws_subprotocol) or (self.ws_subprotocol is not None and resp.get('Sec-Websocket-Protocol') != self.ws_subprotocol):
                    raise WSHandshakeError('The response\'s value of Sec-WebSocket-Protocol does not match the requested value!')

                else:
                    wrap_websocket(self.conn.client, mask = True)

                    self._resp = resp
                    self.connected = 2

                    async def sync_handler(f):
                        f(self.conn.client, resp)

                    async with trio.open_nursery() as nursery:
                        for f in self._on_connect:
                            if inspect.iscoroutinefunction(f):
                                nursery.start_soon(f, self.conn.client, resp)

                            else:
                                nursery.start_soon(sync_handler, f)

    def close(self):
        if self.running:
            self.conn.stop()
            self.running = False

    async def run_loop(self):
        """
        Runs this connection's event loop, without
        connecting. One may manually call the connect
        method afterwards.
        """

        if self.running:
            raise RuntimeError("This websocket is already running!")

        else:
            self.running = True
            await self.conn.client.loop()

    async def connect_run(self, path, subprotocol = None, tls = False, cert_mode = tcpserver.CertMode.CM_GENERATED, fn_component = '', cert_file = None, key_file = None, key_size = 2048):
        """
        Starts this WebSocket connection.
        
        Keyword Arguments:
            path {str} -- Which HTTP endpoint to connect this WebSocket client to.
        """

        if fn_component:
            if key_file is None:
                key_file = ".{}.key.pem".format(fn_component)

            if cert_file is None:
                cert_file = ".{}.cert.pem".format(fn_component)

        await self.connect(path, subprotocol = subprotocol, tls = tls, cert_mode = cert_mode, cert_file = cert_file, key_file = key_file, key_size = key_size)
        await self.run_loop()

    async def connect(self, path, subprotocol = None, tls = False, cert_mode = tcpserver.CertMode.CM_GENERATED, fn_component = '', cert_file = None, key_file = None, key_size = 2048):
        """
        Connects this WebSocket without running the main event loop.
        Use if run_loop was already called, or if run_loop is yet
        to be called.
        
        Keyword Arguments:
            path {str} -- Which HTTP endpoint to connect this WebSocket client to.
        """

        if fn_component:
            if key_file is None:
                key_file = ".{}.key.pem".format(fn_component)

            if cert_file is None:
                cert_file = ".{}.cert.pem".format(fn_component)

        if self.connected:
            raise ConnectionError("This socket is already connected!")

        self.path = path
    
        self.ws_key = os.urandom(16)

        ws_key_header = base64.b64encode(self.ws_key).decode('utf-8')

        sha1 = hashlib.sha1(ws_key_header.encode('utf-8') + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')

        self.ws_accept = sha1.digest()

        self.ws_subprotocol = subprotocol

        headers = {
            'Connection': 'keep-alive, Upgrade',
            'Upgrade': 'websocket',
            'Sec-WebSocket-Key': ws_key_header,
            'Sec-WebSocket-Version': 13
        }

        if subprotocol is not None:
            headers['Sec-WebSocket-Protocol'] = subprotocol

        await self.conn.request(path, headers = headers, tls = tls, cert_mode = cert_mode, cert_file = cert_file, key_file = key_file, key_size = key_size)