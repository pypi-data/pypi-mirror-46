import logging
import os.path
from abc import ABC, abstractmethod
from collections.abc import Mapping, MutableMapping

import yaml

from packy_agent.utils.misc import get_lazy_value, SENTINEL

logger = logging.getLogger(__name__)


class ReadOnlyEmptyDict(Mapping):
    def __getitem__(self, item):
        raise KeyError(item)

    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


READ_ONLY_EMPTY_DICT = ReadOnlyEmptyDict()


class ConfigurationSourceBase(ABC, Mapping):
    is_writeable = False

    def __init__(self, name=None):
        self._is_preparing = False
        self._name = name

    @property
    def is_preparing(self):
        return self._is_preparing

    @property
    @abstractmethod
    def is_ready(self):
        raise NotImplementedError('Must be implemented in child class')

    @property
    def name(self):
        return self._name or self.__class__.__name__


class MappingBackedSource(ConfigurationSourceBase):

    def __init__(self, mapping=None, name=None):
        super().__init__(name=name)

        self._mapping = None

        if mapping is not None:
            self.mapping = mapping

    def __getitem__(self, item):
        return self.mapping[item]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __contains__(self, item):
        return item in self.mapping

    def __eq__(self, other):
        return self.mapping == other

    def __ne__(self, other):
        return self.mapping != other

    def keys(self):
        return self.mapping.keys()

    def items(self):
        return self.mapping.items()

    def values(self):
        return self.mapping.values()

    def get(self, key, default=None):
        logger.debug(f'GET "{self.name}" -> {key}')
        value = self.mapping.get(key, default)
        repr_value = 'SENTINEL' if value is SENTINEL else repr(value)
        logger.debug(f'GOT "{self.name}" -> {key} = {repr_value}')
        return value

    def get_mapping(self):
        return READ_ONLY_EMPTY_DICT if self._mapping is None else self._mapping

    def set_mapping(self, value):
        if value is not None and not isinstance(value, Mapping):
            raise TypeError("'mapping' must be an instance of 'Mapping' or None, but it is '{}'".format(
                type(value).__name__))

        self._mapping = value

    @property
    def is_ready(self):
        return self._mapping is not None

    def ensure_ready(self):
        pass

    @property
    def mapping(self):
        return self.get_mapping()

    @mapping.setter
    def mapping(self, value):
        self.set_mapping(value)


class FileBackedSource(MappingBackedSource, ABC):

    def __init__(self, filename, name=None):

        self._filename = filename
        self._mtime = None
        super().__init__(name=name)

    @staticmethod
    @abstractmethod
    def deserialize(stream):
        raise NotImplementedError('Must be implemented in child class')

    @property
    def filename(self):
        self._filename = get_lazy_value(self._filename)
        return self._filename

    def ensure_ready(self):
        if self.is_ready or self.is_preparing:
            return

        self.get_mapping()

    def get_mapping(self):
        if self._is_preparing:
            return super().get_mapping()

        self._is_preparing = True

        filename = self.filename

        try:
            try:
                mtime = os.path.getmtime(filename)
                if self._mapping is None or self._mtime != mtime:
                    with open(filename) as f:
                        conf = self.deserialize(f)

                    if not isinstance(conf, Mapping):
                        raise TypeError(f'{self.filename} must be a mapping on a root level')

                    self.set_mapping(conf)
                    self._mtime = mtime
            except FileNotFoundError:
                pass
            except OSError:
                logger.exception('Error while reading settings file: %s', filename)

            return super().get_mapping()
        finally:
            self._is_preparing = False

    @property
    def name(self):
        return super().name + f' ({self.filename})'


class YamlFileBackedSource(FileBackedSource):

    @staticmethod
    def deserialize(stream):
        return yaml.load(stream)


class MutableMappingBackedSource(MappingBackedSource, MutableMapping):
    def __setitem__(self, key, value):
        self.mapping[key] = value

    def __delitem__(self, key):
        del self.mapping[key]

    def pop(self, key):
        return self.mapping.pop(key)

    def popitem(self):
        return self.mapping.popitem()

    def clear(self):
        self.mapping.clear()

    def update(self, *args, **kwargs):
        self.mapping.update(*args, **kwargs)

    def setdefault(self, *args, **kwargs):
        return self.mapping.setdefault(*args, **kwargs)
