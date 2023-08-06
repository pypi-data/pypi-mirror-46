import os

import pytest

from packy_agent.configuration.sources.key_value_storage import KeyValueStorageBackedSource

DATABASE_FILENAME = '/tmp/packy-agent-test-settings-database.sqlite3'
TABLENAME = 'test_kv'


@pytest.fixture
def key_value_storage_source():

    try:
        os.remove(DATABASE_FILENAME)
    except FileNotFoundError:
        pass

    return KeyValueStorageBackedSource(TABLENAME, DATABASE_FILENAME)
