from asyncio import Event, get_event_loop
from base64 import b64encode, b64decode
from functools import wraps
from struct import pack, unpack
from urllib.parse import urlparse

import grpc
from math import ceil
from quart import Quart, request

UNCOMPRESSED = 0x00
COMPRESSED = 0x01

MESSAGE = 0x00
TRAILERS = 0x80


def bytes_generator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return b''.join(func(*args, **kwargs))
    return wrapper


@bytes_generator
def encode(*messages):
    for message in messages:
        if isinstance(message, dict):
            message = b''.join(f'{key}:{value}\r\n'.encode('ascii') for key, value in message.items())
            message_type = TRAILERS
        else:
            message_type = MESSAGE

        compressed_flag = bytes([message_type | UNCOMPRESSED])
        message_length = pack('>I', len(message))
        yield b64encode(compressed_flag + message_length + message)


class StreamDecoder:
    def __init__(self, data):
        self.data = data
        self.buffer = bytearray()

    def __getitem__(self, idx):
        if isinstance(idx, int):
            idx = slice(idx, idx + 1, 1)
        elif idx.start and idx.start < 0:
            raise ValueError('Start must be non-negative')
        elif idx.step and idx.step < 1:
            raise ValueError('Step must be positive')
        elif not idx.stop or idx.stop < 0:
            raise ValueError('Stop must be non-negative')

        distance = idx.stop - len(self.buffer)
        if distance > 0:
            cutoff = 4 * ceil(distance / 3)
            data, self.data = self.data[:cutoff], self.data[cutoff:]
            self.buffer += b64decode(data)

            if len(data) < cutoff or len(self.buffer) < idx.stop:
                raise ValueError('Unexpected end of data')

        return bytes(self.buffer[idx])

    @property
    def has_data(self):
        return bool(self.data)

    def flush(self):
        self.buffer = bytearray()


def list_generator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wrapper


@list_generator
def decode(data):
    base64_decoder = StreamDecoder(data)
    while base64_decoder.has_data:
        base64_decoder.flush()

        compressed_flag, message_length = base64_decoder[0], base64_decoder[1:5]
        compressed_flag = compressed_flag[0]
        message_length = unpack('>I', message_length)[0]

        if compressed_flag == COMPRESSED:
            raise NotImplementedError

        message = base64_decoder[5:5 + message_length]
        if compressed_flag & TRAILERS:
            message = message.decode('ascii').rstrip()
            yield dict(entry.split(':', maxsplit=1) for entry in message.split('\r\n'))
        else:
            yield message


def cors(request_headers, allowed_origins=None):
    response_headers = {}

    if 'access-control-request-method' in request_headers:
        response_headers['access-control-allow-methods'] = 'POST'

    if 'access-control-request-headers' in request_headers:
        headers = request_headers['access-control-request-headers'].split(',')
        response_headers['access-control-allow-headers'] = ','.join(
            standard_headers() |
            grpc_headers(headers) |
            grpc_web_client_headers())

    if 'origin' in request_headers:
        if allowed_origins:
            origin = request_headers['origin']
            if urlparse(origin).netloc in allowed_origins:
                response_headers['access-control-allow-origin'] = origin
        else:
            response_headers['access-control-allow-origin'] = '*'

    response_headers['access-control-expose-headers'] = ','.join(
        grpc_headers(request_headers.keys()) |
        grpc_web_server_headers())
    response_headers['access-control-max-age'] = '600'

    return response_headers


def standard_headers():
    return {'content-type'}


def grpc_headers(headers):
    return {header for header in headers if header.islower()} - grpc_web_client_headers() - standard_headers()


def grpc_web_client_headers():
    return {'x-grpc-web',
            'x-user-agent',
            'x-accept-content-transfer-encoding',
            'x-accept-response-streaming',
            'grpc-timeout'}


def grpc_web_server_headers():
    return {'grpc-status',
            'grpc-message'}


def proxy(target,
          credentials=None,
          options=None,
          allowed_origins=None,
          max_timeout=20,
          max_message_size=1024 * 1024 * 4):
    app = Quart('grpcio-helpers')
    if credentials:
        channel = grpc.secure_channel(target, credentials, options)
    else:
        channel = grpc.insecure_channel(target, (options or []) + [
            ('grpc.max_send_message_length', max_message_size),
            ('grpc.max_receive_message_length', max_message_size)
        ])

    @app.route('/<service>/<method>', methods=['POST', 'OPTIONS'])
    async def handler(service, method):
        if request.method == 'OPTIONS':
            return b'', 204, cors(request.headers, allowed_origins)
        elif not request.headers.get('content-type', '').startswith('application/grpc'):
            return b'', 415

        timeout = min(float(request.headers.get('grpc-timeout', 'inf')), max_timeout)
        request_message = decode(await request.get_data())[0]
        request_metadata_keys = grpc_headers(request.headers)
        request_metadata = [(key, request.headers[key]) for key in request_metadata_keys]
        caller = channel.unary_unary(f'/{service}/{method}')
        future = caller.future(request_message, timeout=timeout, metadata=request_metadata)

        loop = get_event_loop()
        done = Event()
        future.add_done_callback(lambda _: loop.call_soon_threadsafe(done.set))
        await done.wait()

        headers = {
            **cors(request.headers, allowed_origins),
            **dict(future.initial_metadata()),
            'content-type': 'application/grpc-web-text+proto'}
        trailers = {
            **dict(future.trailing_metadata()),
            **{'grpc-status': str(future.code().value[0]),
               'grpc-message': future.details() or future.code().name}}

        if future.exception():
            return b'', 200, {**headers, **trailers}
        else:
            return encode(future.result(), trailers), 200, headers

    return app
