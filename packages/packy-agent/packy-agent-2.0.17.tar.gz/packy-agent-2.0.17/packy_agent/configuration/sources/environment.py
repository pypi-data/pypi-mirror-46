import os
from collections import OrderedDict

from packy_agent.configuration.sources.base import MappingBackedSource
from packy_agent.configuration.base import NESTING_PREFIXES
from packy_agent.utils.misc import yaml_coerce
from packy_agent.utils.collections import deep_update


ENVVAR_PREFIX = 'PACKY_AGENT_'
ENVVAR_PREFIX_LEN = len(ENVVAR_PREFIX)
NESTING_PREFIXES_ = tuple(v.upper() + '_' for v in NESTING_PREFIXES)


def get_settings_key_value(env_key, env_value):
    coerce_value = yaml_coerce(env_value)
    level1_key = env_key[ENVVAR_PREFIX_LEN:]
    for nesting_prefix in NESTING_PREFIXES_:
        if level1_key.startswith(nesting_prefix):
            return {
                nesting_prefix[:-1].lower(): {
                    level1_key[len(nesting_prefix):].lower(): coerce_value
                }
            }

    return {level1_key.lower(): coerce_value}


def is_settings_env_var(env_key):
    return env_key.startswith(ENVVAR_PREFIX)


class Environment(MappingBackedSource):

    def __init__(self, name=None):
        super().__init__(os.environ, name=name)

    def __getitem__(self, item):
        # TODO(dmu) LOW: Provide a faster implementation
        return dict(self.items())[item]

    def __iter__(self):
        yield from self.keys()

    def __contains__(self, item):
        # TODO(dmu) LOW: Provide a faster implementation
        return item in self.keys()

    def keys(self):
        yield from (k for k, _ in self.items())

    def items(self):
        all_items = OrderedDict()
        for key, value in super().items():
            if is_settings_env_var(key):
                deep_update(all_items, get_settings_key_value(key, value))

        yield from all_items.items()

    def values(self):
        yield from (v for _, v in self.items())

    def get(self, key, default=None):
        if not isinstance(key, str):
            raise TypeError("'key' must be a string")

        # TODO(dmu) LOW: Provide a faster implementation
        return dict(self.items()).get(key, default)
