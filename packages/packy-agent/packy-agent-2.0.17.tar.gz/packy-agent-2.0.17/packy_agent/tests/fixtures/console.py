import pytest

from packy_agent.console.app import get_app


@pytest.fixture
def app():
    return get_app()


@pytest.fixture
def console_flask_client(client, config):
    testing = config['TESTING']
    config['TESTING'] = True
    wtf_csrf_enabled = config.get('WTF_CSRF_ENABLED', True)
    config['WTF_CSRF_ENABLED'] = False
    yield client
    config['TESTING'] = testing
    config['WTF_CSRF_ENABLED'] = wtf_csrf_enabled
