import time
import os
import os.path
from contextlib import contextmanager

import yaml
import pytest
from alembic.config import Config
from alembic import command

from packy_agent.utils.pkg_resources import get_package_file_full_path
from packy_agent.configuration.settings import settings
from packy_agent.configuration.sources.base import MappingBackedSource

CONFIG_ENV_VAR_NAME = 'PACKY_AGENT_SETTINGS_FILENAME'


def prefix_filename(path, prefix='test-'):
    head, tail = os.path.split(path)
    return os.path.join(head, prefix + tail)


@pytest.fixture(scope='session', autouse=True)
def test_config():
    config_path = os.environ.get(CONFIG_ENV_VAR_NAME)
    if not config_path:
        raise Exception(f'Environment variable {CONFIG_ENV_VAR_NAME} is not defined')

    with open(config_path) as f:
        local_config = yaml.load(f)

    database_filename = local_config.get('database_filename')
    if not database_filename:
        raise Exception(f'database_filename key is not defined in {config_path}')

    test_config_path = prefix_filename(config_path)
    try:
        os.remove(test_config_path)
    except FileNotFoundError:
        pass

    # TODO(dmu) LOW: Maybe use `override_settings` instead?
    # Make timeouts smaller
    local_config['worker']['consumer_loop_timeout'] = 0.1
    local_config['worker']['results_submission_period_seconds'] = 0.1
    local_config['worker']['results_submission_pause_seconds'] = 0.1
    local_config['worker']['purge_period_seconds'] = 1
    local_config['worker']['loops'] = [
        'ping_module', 'trace_module', 'http_module', 'speedtest_module', 'consumer', 'submitter',
        'purger']

    # Substitute names
    local_config['database_filename'] = prefix_filename(database_filename)
    local_config['server_base_url'] = 'http://test'
    local_config['communication_url'] = 'ws://test/ws'
    local_config['sentry_dns'] = None

    with open(test_config_path, 'w') as f:
        yaml.dump(local_config, f, default_flow_style=False)

    os.environ[CONFIG_ENV_VAR_NAME] = test_config_path

    return test_config_path


@pytest.fixture(autouse=True)
def local_database(test_config):
    from packy_agent.configuration.settings import settings
    database_filename = settings.get_database_filename()
    # At this moment key-value storage tables are created
    try:
        os.remove(database_filename)
    except FileNotFoundError:
        pass

    # Recreate key-value storage tables
    settings._local_settings._mapping = None
    settings._cached_settings._mapping = None

    alembic_cfg = Config(get_package_file_full_path('packy_agent', 'configuration/alembic.ini'))
    command.upgrade(alembic_cfg, 'head')


@pytest.fixture(autouse=True)
def logging(test_config):
    from packy_agent.utils.logging import configure_logging
    configure_logging()


@pytest.fixture
def activated():
    from packy_agent.configuration.settings import settings

    settings.activate(
        client_id='client_id',
        access_token='access_token_value',
        refresh_token='refresh_token_value',
        agent_key='agent_key_value',
        agent_name='name_value',
    )


@contextmanager
def override_setting(key, value):
    settings._sources.insert(0, MappingBackedSource({key: value}))
    yield
    settings._sources.pop(0)


@contextmanager
def override_settings(new_settings):
    settings._sources.insert(0, MappingBackedSource(new_settings))
    yield
    settings._sources.pop(0)


@contextmanager
def local_settings(new_settings):
    from packy_agent.configuration.settings import settings
    backup = {}
    for k, v in new_settings.items():
        if k in settings._local_settings:
            backup[k] = settings._local_settings[k]

    # TODO(dmu) LOW: Implement deep update here
    settings._local_settings.update(new_settings)
    yield
    settings._local_settings.update(backup)


@pytest.fixture
def watchdog_started_long_ago():
    with override_settings({'watchdog': {'started_at_ts': time.time() - 3600}}):
        yield
