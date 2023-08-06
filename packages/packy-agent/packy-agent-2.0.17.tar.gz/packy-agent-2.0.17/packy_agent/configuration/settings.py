import time
import re
import logging
from functools import partial
from collections import OrderedDict
import threading
from collections import Mapping

from packy_agent.exceptions import ImproperlyConfiguredError
from packy_agent.utils.misc import SENTINEL, yaml_coerce
from packy_agent.configuration.sources.base import MappingBackedSource, MutableMappingBackedSource
from packy_agent.configuration.sources.key_value_storage import KeyValueStorageBackedSource
from packy_agent.configuration.sources.defaults import ConfigurationDefaults
from packy_agent.configuration.sources.environment import Environment
from packy_agent.configuration.sources.file import File as FileSource
from packy_agent.configuration.sources.server import Server as ServerSource
from packy_agent.utils.collections import deep_update
from packy_agent.configuration.base import SUPERVISOR, CONSOLE, WORKER, WATCHDOG


TABLENAME = 'settings'
GETTER_PREFIX = 'get_'
IS_PREFIX = 'is_'
SETTER_PREFIX = 'set_'

METHOD_PATTERN_RE = re.compile(
    f'^(?P<type>{GETTER_PREFIX}|{IS_PREFIX}|{SETTER_PREFIX})'
    f'(?:(?P<section>{WORKER}|{CONSOLE}|{WATCHDOG}|{SUPERVISOR})_)?(?P<key>.*)?')


logger = logging.getLogger(__name__)
threading_local = threading.local()


# TODO(dmu) MEDIUM: Implement ConfigurationSourceBase interface?
class Settings:

    def __init__(self):
        # Prefilled with 'invalid_access_tokens' for optimization purposes
        self._runtime = MutableMappingBackedSource({'invalid_access_tokens': set()},
                                                   name='Local runtime')

        self._key_value_storage = None
        self._commandline_arguments = {}

        self._cached_settings = KeyValueStorageBackedSource(
            self.get_cached_settings_tablename, self.get_key_value_storage_filename,
            name='Cached'
        )
        self._server_source = ServerSource(
            persist_callable=lambda x: self._cached_settings.replace(x),
            name='From server',
        )

        self._local_settings = KeyValueStorageBackedSource(
            self.get_local_settings_tablename, self.get_key_value_storage_filename,
            name='Local',
        )

        self._sources = [
            self._runtime,
            MappingBackedSource(self._commandline_arguments, name='From command line'),
            Environment(name='From environment variables'),
            self._server_source,
            self._cached_settings,
            self._local_settings,
            FileSource(self.get_settings_filename, name='Settings file'),
            ConfigurationDefaults(),
        ]

    def __getattr__(self, item):
        if isinstance(item, str):
            match = METHOD_PATTERN_RE.match(item)
            if match:
                type_ = match.group('type')
                section = match.group('section')
                key = match.group('key')
                if type_ in (GETTER_PREFIX, IS_PREFIX):
                    if section:
                        return partial(self.get_subkey, section, key)
                    else:
                        return partial(self.get, key)
                elif type_ == SETTER_PREFIX:
                    if section:
                        return partial(self.set_subkey, section, key)
                    else:
                        return partial(self.set, key)
                else:
                    raise ValueError(f'Unknown prefix {type_}')  # should never get here

        raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__, item))

    def labeled_items(self):
        for source in self._sources:
            yield source.name, source.items() if source.is_ready else ()

    def items(self):
        items = OrderedDict()
        for source in reversed(self._sources):
            items.update(source.items())

        return items

    def get(self, key, default=None):
        sources = self._sources
        for source in sources:
            source.ensure_ready()

        sources_iterator = iter(sources)
        for source in sources_iterator:
            if not source.is_ready:
                continue

            value = source.get(key, SENTINEL)
            if value is not SENTINEL:
                if isinstance(value, Mapping):
                    # This part is about deep update (for logging configuration mostly)
                    last_value = value
                    new_value = {}
                    for deeper_source in reversed(list(sources_iterator)):
                        if deeper_source.is_ready:
                            value = deeper_source.get(key, SENTINEL)
                            if value is not SENTINEL:
                                deep_update(new_value, value)

                    deep_update(new_value, last_value)
                    value = new_value

                break
        else:
            value = default

        return value

    def get_subkey(self, key, subkey, default=None):
        return (self.get(key) or {}).get(subkey, default)

    def set(self, key, value):
        coerced_value = yaml_coerce(value)
        try:
            self._local_settings[key] = coerced_value
        except TypeError:
            raise ImproperlyConfiguredError(
                f'Unable to set {key}={value!r}: local settings key value storage is '
                f'not configured')

    def set_subkey(self, key, subkey, value):
        super_value = self._local_settings.get(key)
        super_value = super_value.copy() if super_value else {}
        super_value[subkey] = value
        self.set(key, super_value)

    def set_runtime(self, key, value):
        self._runtime[key] = value

    def delete(self, key):
        try:
            del self._local_settings[key]
        except TypeError:
            raise ImproperlyConfiguredError(
                "Unable to delete '{}': local settings key value storage is "
                "not configured".format(key))

    def clear(self):
        self._local_settings.clear()

    def set_commandline_arguments(self, arguments):
        self._commandline_arguments.clear()
        self._commandline_arguments.update(arguments)

    def validate(self):
        if not self.get_server_base_url():
            raise ImproperlyConfiguredError("'server_base_url' must be explicitly set")
        if not self.get_component():
            raise ImproperlyConfiguredError("'component' must be explicitly set")

    def activate(self, client_id, access_token, refresh_token, agent_key, agent_name):
        self.set('client_id', client_id)  # needed for refresh token only
        self.set('access_token', access_token)
        self.set('refresh_token', refresh_token)
        self.set('agent_key', agent_key)
        self.set('agent_name', agent_name)
        self.set('activated', True)

        self._server_source.expire_cache()

    def deactivate(self):
        self.delete('client_id')
        self.delete('access_token')
        self.delete('refresh_token')
        self.delete('agent_key')
        self.delete('agent_name')
        self.set('activated', False)

    def has_settings_changed_on_server(self):
        self._server_source.get_mapping()  # to update `has_changed` attribute
        return self._server_source.has_changed

    def update_started_at_ts(self, component=None):
        component = component or self.get_component()
        if not component:
            raise ImproperlyConfiguredError('Component must be provided')

        self.set_subkey(component, 'started_at_ts', time.time())

    def update_restarted_at_ts(self, component):
        self.set_subkey(component, 'restarted_at_ts', time.time())

    def update_rebooted_at_ts(self, delta=0):
        self.set('rebooted_at_ts', time.time() + delta)

    #######################################
    # Explicit settings getters and setters

    def get_log_level(self):
        return self.get('log_level')

    def get_settings_filename(self):
        return self.get('settings_filename')

    def get_database_filename(self):
        return self.get('database_filename')

    def get_key_value_storage_filename(self):
        return self.get_database_filename()

    def get_database_url(self):
        database_filename = self.get_database_filename()
        if database_filename:
            return 'sqlite:///' + database_filename

    def get_cached_settings_tablename(self):
        return self.get('cached_settings_tablename')

    def get_local_settings_tablename(self):
        return self.get('local_settings_tablename')

    def get_server_base_url(self):
        server_base_url = self.get('server_base_url')
        if server_base_url:
            return server_base_url.rstrip('/') + '/'

    def get_console_base_url(self, ip_address=None):
        from packy_agent.utils.network import get_actual_ip_address
        # TODO(dmu) LOW: Unhardcode schema: `http://`
        ip_address = ip_address or get_actual_ip_address()
        url = 'http://' + ip_address
        port = self.get_console_http_port()
        if port != 80:
            url += f':{port}'

        return url + '/'

    def set_console_flask_secret_key(self, key):
        mapping = self.get_console_flask()
        mapping = mapping.copy() if mapping else {}
        mapping['SECRET_KEY'] = key
        self.set_console_flask(mapping)

    def get_current_component_setting(self, key, default=None):
        component = self.get_component()
        if not component:
            return default

        return self.get_subkey(component, key, default=default)

    def reset_network_data_usage(self):
        self.delete('bytes_sent')
        self.delete('bytes_received')


# We need all greenlets to share the same settings object to share runtime-settings
# (stored in RAM only) and to avoid excess access to externally stored settings
# (i.e. on Packy Server)
settings = Settings()
