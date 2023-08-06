import asyncio
import re
import sys
from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import grpc
import hypercorn.asyncio
import hypercorn.config

from grpc_helpers.proxy import proxy

_servers = []


def _identities(cls):
    yield cls
    for base in cls.__bases__:
        yield from _identities(base)


def _parse_binding(binding):
    match = re.fullmatch(r'\[?(?P<address>.*?)\]?(?::(?P<port>[0-9]+))?', binding)
    return match['address'], match['port'] or '0'


def serve(
        *services,
        credentials=None,
        options=None,
        bindings=None,
        web_bindings=None,
        max_workers=10,
        max_message_size=1024 * 1024 * 4,
        block=True):
    executor = ThreadPoolExecutor(max_workers=max_workers)
    grpc_server = grpc.server(executor, options=(options or []) + [
        ('grpc.max_send_message_length', max_message_size),
        ('grpc.max_receive_message_length', max_message_size)
    ])

    for service in services:
        for cls in _identities(service.__class__):
            if hasattr(sys.modules[cls.__module__], f'add_{cls.__name__}_to_server'):
                getattr(sys.modules[cls.__module__], f'add_{cls.__name__}_to_server')(service, grpc_server)
                break
        else:
            raise ValueError(f'Class "{service.__class__.__name__}" is not a gRPC service')

    if not bindings:
        bindings = ['0.0.0.0:443' if credentials else '0.0.0.0:80']
    if credentials:
        def register_binding(binding):
            return grpc_server.add_secure_port(binding, credentials)
    else:
        def register_binding(binding):
            return grpc_server.add_insecure_port(binding)
    bindings = {(_parse_binding(binding)[0], str(register_binding(binding))) for binding in bindings}

    grpc_server.start()
    _servers.append(grpc_server)

    if web_bindings:
        binding = next(iter(bindings))
        binding = next((('::1', port) for addr, port in bindings if addr in {'::', '::1'}), binding)
        binding = next((('127.0.0.1', port) for addr, port in bindings if addr in {'0.0.0.0', '127.0.0.1'}), binding)
        address, port = binding
        app = proxy(f'{f"[{address}]" if ":" in address else address}:{port}', max_message_size=max_message_size)

        config = hypercorn.config.Config()
        config.bind = list(map(':'.join, map(_parse_binding, web_bindings)))
        web_server = hypercorn.asyncio.serve(app, config)

        try:
            return grpc_server, get_running_loop().create_task(web_server)
        except RuntimeError:
            asyncio.run(web_server)
    elif block:
        Event().wait()

    return grpc_server
