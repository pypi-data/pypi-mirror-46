import binascii
import os
import logging
import random
import distutils
import cachetools

import yaml

from atomicwrites import AtomicWriter, atomic_write as atomic_write_original
from packy_agent.utils.cache import custom_cached


SENTINEL = object()


logger = logging.getLogger(__name__)


def yaml_coerce(value):
    if isinstance(value, str):
        return yaml.load('dummy: ' + value)['dummy']

    return value


@custom_cached(cachetools.TTLCache(100, ttl=1))
def get_lazy_value(value):
    return value() if hasattr(value, '__call__') else value


def get_executable_path(executable, self_failover=True):
    path = distutils.spawn.find_executable(executable)
    if not path and self_failover:
        path = executable

    return path


class CustomAtomicWriter(AtomicWriter):
    def commit(self, f):
        path = self._path
        if os.path.isfile(path):
            filestat = os.stat(path)
        else:
            filestat = None

        super(CustomAtomicWriter, self).commit(f)

        if filestat is not None:
            try:
                os.chmod(path, filestat.st_mode)
                os.chown(path, filestat.st_uid, filestat.st_gid)
            except Exception:
                logger.warning('Failed to restore permissions or ownership for file: %s', path)


def atomic_write(path, writer_cls=CustomAtomicWriter, **cls_kwargs):
    return atomic_write_original(path=path, writer_cls=writer_cls, **cls_kwargs)


def generate_random_string(size_bytes):
    return (('{:0' + str(size_bytes) + 'x}').format(random.getrandbits(size_bytes * 4))
            if size_bytes else '')


def generate_flask_secret_key():
    return generate_random_string(128)


def safe_hexlify(data):
    return binascii.hexlify(data).decode() if data else data
