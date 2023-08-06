import json
from collections import MutableMapping

from sqlitedict import SqliteDict

from packy_agent.configuration.sources.base import (
    ConfigurationSourceBase, READ_ONLY_EMPTY_DICT)
from packy_agent.utils.misc import get_lazy_value
from packy_agent.utils.gevent import database_locks


def key_value_encode(obj):
    return json.dumps(obj)


def key_value_decode(obj):
    return json.loads(obj)


class KeyValueStorageBackedSource(ConfigurationSourceBase, MutableMapping):

    is_writeable = True

    def __init__(self, tablename=None, filename=None, name=None):
        self._tablename = tablename
        self._filename = filename

        self._mapping = None

        super().__init__(name=name)

    def __getitem__(self, item):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping[item]

    def __iter__(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                yield from mapping

    def __len__(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return len(mapping)

    def __contains__(self, item):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return item in mapping

    def __eq__(self, other):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping == other

    def __ne__(self, other):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping != other

    def __setitem__(self, key, value):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                mapping[key] = value

    def __delitem__(self, key):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                del mapping[key]

    def keys(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                yield from mapping.keys()

    def items(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                yield from mapping.items()

    def values(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                yield from mapping.values()

    def get(self, key, default=None):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping.get(key, default)

    def pop(self, key):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping.pop(key)

    def popitem(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping.popitem()

    def clear(self):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                mapping.clear()

    def update(self, *args, **kwargs):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                mapping.update(*args, **kwargs)

    def setdefault(self, *args, **kwargs):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                return mapping.setdefault(*args, **kwargs)

    def replace(self, new_mapping):
        with database_locks[self.filename]:
            with self.get_mapping() as mapping:
                mapping.clear()
                mapping.update(new_mapping)

    @property
    def is_ready(self):
        return (isinstance(self._tablename, str) and isinstance(self._filename, str) and
                self._mapping is not None)

    def ensure_ready(self):
        if self.is_ready or self.is_preparing:
            return

        self.get_mapping()

    @property
    def tablename(self):
        self._tablename = get_lazy_value(self._tablename)
        return self._tablename

    @property
    def filename(self):
        self._filename = get_lazy_value(self._filename)
        return self._filename

    def get_mapping(self):
        if self._mapping is None and not self._is_preparing:
            self._is_preparing = True
            try:
                filename = self.filename
                tablename = self.tablename
                if filename and tablename:
                    self._mapping = SqliteDict(
                        filename, tablename=tablename, autocommit=True, encode=key_value_encode,
                        decode=key_value_decode)
            finally:
                self._is_preparing = False

        return READ_ONLY_EMPTY_DICT if self._mapping is None else self._mapping
