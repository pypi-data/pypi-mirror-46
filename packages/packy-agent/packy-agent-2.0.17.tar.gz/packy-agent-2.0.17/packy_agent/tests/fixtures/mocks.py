import pytest

from packy_agent.clients.sentry import init_sentry_client


@pytest.fixture(scope='session', autouse=True)
def sentry_server_mock(test_config):
    events = []

    def capture(event):
        events.append(event)

    init_sentry_client(packy_agent_sentry_dsn='https://dummy:dummy@dummy.dummy/1',
                       transport=capture)

    return events
