import json
from urllib.parse import urlparse

import flask
import httpretty
import pytest

from packy_agent.configuration.settings import settings
from packy_agent.tests.fixtures.configuration import override_settings


@pytest.mark.usefixtures('activated')
def test_login_logout(console_flask_client):
    agent_key = 'agent_key_value'
    assert settings.is_activated()

    response = console_flask_client.get('/')
    assert response.status_code == 302
    assert urlparse(response.location).path == '/login/'

    response = console_flask_client.get('/login/')
    assert response.status_code == 200

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/user/agent/'
        httpretty.register_uri(
            httpretty.GET, url,
            body=json.dumps([{'key': agent_key, 'user': {'email': 'test@test.com'}}]))

        response = console_flask_client.post(
            '/login/', data={'email': 'test@test.com', 'password': 'test'},
            follow_redirects=True)
        assert response.status_code == 200
        assert flask.session['agent_key'] == agent_key

        latest_requests = httpretty.HTTPretty.latest_requests
        assert len(latest_requests) == 1
        assert latest_requests[0].method == 'GET'
        assert (latest_requests[0].path ==
                f'/api/v2/user/agent/?fields=key%2Cuser&expand=user&key={agent_key}')

    response = console_flask_client.get('/')
    assert response.status_code == 200

    response = console_flask_client.post('/logout/', follow_redirects=True)
    assert response.status_code == 200
    assert 'agent_key' not in flask.session

    response = console_flask_client.get('/')
    assert response.status_code == 302
    assert urlparse(response.location).path == '/login/'
