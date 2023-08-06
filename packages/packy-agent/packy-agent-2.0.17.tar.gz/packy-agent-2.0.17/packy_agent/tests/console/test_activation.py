import json

import pytest
import httpretty

from urllib.parse import urlparse
from packy_agent.configuration.settings import settings


def test_activation(console_flask_client):
    assert not settings.is_activated()

    response = console_flask_client.get('/activate/')
    assert response.status_code == 200

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/user/agent/'
        httpretty.register_uri(httpretty.GET, url, body='[]')
        httpretty.register_uri(
            httpretty.POST, url, status=201,
            body=json.dumps({
                'access_token': 'access_token',
                'refresh_token': 'refresh_token',
                'key': 'key',
                'name': 'name',
                'client_id': 'client_id',
            }))

        response = console_flask_client.post(
            '/activate/', data={'email': 'test@test.com', 'password': 'test'},
            follow_redirects=True)
        assert response.status_code == 200

        latest_requests = httpretty.HTTPretty.latest_requests
        assert len(latest_requests) >= 2
        assert latest_requests[0].path == '/api/v2/user/agent/?fields=id%2Cname&is_active=false'
        assert latest_requests[0].method == 'GET'
        assert latest_requests[1].path == '/api/v2/user/agent/'
        assert latest_requests[1].method == 'POST'
        body = json.loads(latest_requests[1].body)
        assert 'name' in body
        assert isinstance(body['name'], str)

    assert settings.is_activated()


def test_activation_invalid_password(console_flask_client):
    assert not settings.is_activated()

    response = console_flask_client.get('/activate/')
    assert response.status_code == 200

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/user/agent/'
        httpretty.register_uri(httpretty.GET, url, status=401)

        response = console_flask_client.post(
            '/activate/', data={'email': 'test@test.com', 'password': 'test'})
        assert response.status_code == 302
        assert urlparse(response.location).path == '/activation-failure/'

    assert not settings.is_activated()


@pytest.mark.parametrize('http_status', (500, 501, 502, 503, 504))
def test_activation_server_http5xx(console_flask_client, http_status):
    assert not settings.is_activated()

    response = console_flask_client.get('/activate/')
    assert response.status_code == 200

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/user/agent/'
        httpretty.register_uri(httpretty.GET, url, status=http_status)

        response = console_flask_client.post(
            '/activate/', data={'email': 'test@test.com', 'password': 'test'})
        assert response.status_code == 302
        assert urlparse(response.location).path == '/activation-failure/'

    assert not settings.is_activated()


@pytest.mark.parametrize('http_status', (400, 401, 403, 404, 405, 406, 408, 429))
def test_activation_server_http4xx(console_flask_client, http_status):
    assert not settings.is_activated()

    response = console_flask_client.get('/activate/')
    assert response.status_code == 200

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/user/agent/'
        httpretty.register_uri(httpretty.GET, url, status=http_status)

        response = console_flask_client.post(
            '/activate/', data={'email': 'test@test.com', 'password': 'test'})
        assert response.status_code == 302
        assert urlparse(response.location).path == '/activation-failure/'

    assert not settings.is_activated()


def test_activation_server_connection_error(console_flask_client):
    assert not settings.is_activated()

    response = console_flask_client.get('/activate/')
    assert response.status_code == 200

    response = console_flask_client.post(
        '/activate/', data={'email': 'test@test.com', 'password': 'test'})
    assert response.status_code == 302
    assert urlparse(response.location).path == '/activation-failure/'

    assert not settings.is_activated()
