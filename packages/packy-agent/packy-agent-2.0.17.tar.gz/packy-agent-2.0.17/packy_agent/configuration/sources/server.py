import time
import logging

from requests.exceptions import ConnectionError, HTTPError

from packy_agent.exceptions import ImproperlyConfiguredError, NoAccessTokenError
from packy_agent.configuration.sources.base import MappingBackedSource, READ_ONLY_EMPTY_DICT


logger = logging.getLogger(__name__)


SETTINGS_SUCCESS_CACHE_TIMEOUT_SECONDS = 600
SETTINGS_FAILURE_CACHE_TIMEOUT_SECONDS = 60


class Server(MappingBackedSource):

    def __init__(self, mapping=None, persist_callable=None, name=None):
        super().__init__(mapping, name=name)

        self.has_changed = False
        self._persist_callable = persist_callable
        self._mapping_expire_ts = 0

    def expire_cache(self):
        self._mapping_expire_ts = 0

    def ensure_ready(self):
        if self.is_ready or self.is_preparing:
            return

        self.get_mapping()

    def get_mapping(self):
        from packy_agent.clients.packy_server import get_packy_server_client

        if self._is_preparing:
            return super().get_mapping()

        self._is_preparing = True
        try:
            if time.time() >= self._mapping_expire_ts:
                try:
                    settings = get_packy_server_client().get_settings()
                    if self._persist_callable:
                        self._persist_callable(settings)
                except Exception as ex:
                    if isinstance(ex, ConnectionError):
                        logger.warning('Could not connect to server to get settings')
                    elif isinstance(ex, HTTPError):
                        logger.warning('Error while getting settings from server: %r', ex)
                    elif isinstance(ex, NoAccessTokenError):
                        logger.debug('No access token found. Probably agent is not activated yet')
                    elif isinstance(ex, ImproperlyConfiguredError):
                        logger.warning('Packy Server client was not configured: %s', ex)
                    else:
                        logger.exception('Error while getting settings from server')

                    self._mapping_expire_ts = time.time() + SETTINGS_FAILURE_CACHE_TIMEOUT_SECONDS
                else:
                    prev_mapping = super().get_mapping()
                    self.has_changed = (
                            prev_mapping is not READ_ONLY_EMPTY_DICT and settings != prev_mapping)
                    self.set_mapping(settings)  # To make it `ready`
                    self._mapping_expire_ts = time.time() + SETTINGS_SUCCESS_CACHE_TIMEOUT_SECONDS

            return super().get_mapping()
        finally:
            self._is_preparing = False
