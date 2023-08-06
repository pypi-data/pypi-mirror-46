import json

import flask
import pytest
import httpretty

from urllib.parse import urlparse
from packy_agent.configuration.settings import settings


@pytest.mark.usefixtures('activated')
def test_deactivation(console_flask_client):
    assert settings.is_activated()
    assert not settings.is_worker_stopped()

    # emulate login
    with console_flask_client.session_transaction() as session:
        session['agent_key'] = 'agent_key_value'

    response = console_flask_client.get('/reset/')
    assert response.status_code == 200
    assert flask.session['agent_key'] == 'agent_key_value'

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/agent/'
        httpretty.register_uri(httpretty.PATCH, url, status=200,)

        response = console_flask_client.post('/reset/', data={'action': 'deactivate'})
        assert response.status_code == 302
        assert urlparse(response.location).path == '/success/'

        latest_requests = httpretty.HTTPretty.latest_requests
        assert len(latest_requests) == 1
        assert latest_requests[0].path == '/api/v2/agent/'
        assert latest_requests[0].method == 'PATCH'
        body = json.loads(latest_requests[0].body)
        assert 'is_active' in body
        assert body['is_active'] is False

    assert not settings.is_activated()

    assert settings.get_access_token() is None
    assert settings.get_refresh_token() is None
    assert settings.get_agent_key() is None
    assert settings.get_agent_name() is None

    assert 'agent_key' not in flask.session
