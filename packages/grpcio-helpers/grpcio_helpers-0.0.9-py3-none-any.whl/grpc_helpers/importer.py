import inspect
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from importlib.abc import MetaPathFinder, SourceLoader
from importlib.util import spec_from_loader
from pathlib import Path
from tempfile import TemporaryDirectory

from grpc_tools import protoc
from pkg_resources import resource_filename


@dataclass
class Config:
    save_compiled: bool = False
    extra_args: list = field(default_factory=list)


class ProtoMetaPathFinder(MetaPathFinder):
    configs = defaultdict(Config)
    cache = {}

    @classmethod
    def find_spec(cls, fullname, path, target=None):
        config = cls.config(fullname)
        if not config:
            return None

        *parents, name = fullname.split('.')
        stem, matched = re.subn('_pb2(?:_grpc)?$', '', name)
        if not matched:
            return None

        for entry in map(Path, sys.path if path is None else path):
            proto_file = entry/f'{stem}.proto'
            if proto_file.is_file():
                break
        else:
            return None

        source_file = proto_file.parent/f'{stem}.py'
        if config.save_compiled and \
           source_file.exists() and \
           source_file.stat().st_mtime >= proto_file.stat().st_mtime:
            return None  # Let the normal import machinery handle it

        root = entry
        for parent in reversed(parents):
            if root.name == parent:
                root = root.parent
            else:
                raise ImportError('Cannot compile proto files in packages with unusual __path__')

        if fullname in cls.cache:
            return cls.cache[fullname]
        with TemporaryDirectory() as prefix:
            prefix = Path(prefix)
            cls.compile(prefix, root, proto_file, config.extra_args)

            if config.save_compiled:
                cls.copy(prefix, root)
                return None  # Let the normal import machinery handle the rest
            else:
                relative_prefix = proto_file.parent.relative_to(root)
                cls.populate_cache(base_prefix=prefix, relative_prefix=relative_prefix, stem=stem, name=fullname)
                return cls.cache[fullname]

    @classmethod
    def invalidate_caches(cls):
        cls.cache = {}

    @classmethod
    def config(cls, fullname):
        matches = filter(lambda key: fullname.startswith(key), cls.configs)
        matches = sorted(matches, key=len, reverse=True)
        return cls.configs[matches[0]] if len(matches) else None

    @classmethod
    def compile(cls, prefix, path, proto_file, extra_args):
        command = [
            'grpc_tools.protoc',
            f'--proto_path={path}',
            f'--python_out={prefix}',
            f'--grpc_python_out={prefix}'
        ] + extra_args + [str(proto_file)]

        if protoc.main(command) != 0:
            raise ImportError(f'Failed to compile proto file "{proto_file}"')

    @classmethod
    def copy(cls, source, destination):
        if source.is_dir():
            destination.mkdir(exist_ok=True)

            for item in source.iterdir():
                cls.copy(item, destination/item.name)
        elif source.is_file():
            destination.write_bytes(source.read_bytes())

    @classmethod
    def populate_cache(cls, base_prefix, relative_prefix, stem, name):
        for postfix in ['_pb2', '_pb2_grpc']:
            relative_path = relative_prefix/f'{stem}{postfix}.py'
            absolute_path = base_prefix/relative_path

            if not absolute_path.exists():
                raise ImportError(f'Missing proto artifact "{relative_path}"')

            loader = MemorySourceLoader(filename=str(relative_path), data=absolute_path.read_bytes())
            cls.cache[name] = spec_from_loader(name, loader)


@dataclass
class MemorySourceLoader(SourceLoader):
    filename: str
    data: bytes

    def get_filename(self, fullname):
        return self.filename

    def get_data(self, path):
        return self.data


def register_import_hook(save_compiled=None, well_known_protos=False, extra_args=None):
    if ProtoMetaPathFinder not in sys.meta_path:
        sys.meta_path.insert(0, ProtoMetaPathFinder)

    stack = inspect.stack()
    module = inspect.getmodule(stack[1].frame)
    name = module.__package__ or ''

    if name in ProtoMetaPathFinder.configs:
        raise NameError(f'Import hook for package {name} has already been registered')

    ProtoMetaPathFinder.configs[name] = Config()
    if save_compiled is not None:
        ProtoMetaPathFinder.configs[name].save_compiled = save_compiled
    if well_known_protos:
        ProtoMetaPathFinder.configs[name].extra_args += [f'--proto_path={resource_filename("grpc_tools", "_proto")}']
    if extra_args:
        ProtoMetaPathFinder.configs[name].extra_args += extra_args
