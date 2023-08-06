import json

import httpretty

from packy_agent.configuration.settings import settings


def test_reactivation(console_flask_client):
    assert not settings.is_activated()

    response = console_flask_client.get('/activate/')
    assert response.status_code == 200

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/user/agent/'
        httpretty.register_uri(httpretty.GET, url, body='[{"id": 1, "name": "deactivated"}]')
        httpretty.register_uri(
            httpretty.PATCH, url + '1/', status=200,
            body=json.dumps({
                'client_id': 'client_id',
                'access_token': 'access_token',
                'refresh_token': 'refresh_token',
                'key': 'key',
                'name': 'name',
            }))

        response = console_flask_client.post(
            '/activate/', data={'email': 'test@test.com', 'password': 'test'},
            follow_redirects=True)
        assert response.status_code == 200
        response = console_flask_client.post(
            '/activate/', data={'email': 'test@test.com', 'password': 'test', 'agent': '1',
                                'extra': 'yes'},
            follow_redirects=True)
        assert response.status_code == 200

        latest_requests = httpretty.HTTPretty.latest_requests
        assert len(latest_requests) >= 3
        assert latest_requests[0].method == 'GET'
        assert latest_requests[0].path == '/api/v2/user/agent/?fields=id%2Cname&is_active=false'
        assert latest_requests[1].method == 'GET'
        assert latest_requests[1].path == '/api/v2/user/agent/?fields=id%2Cname&is_active=false'
        assert latest_requests[2].method == 'PATCH'
        assert latest_requests[2].path == '/api/v2/user/agent/1/?with_configuration=yes'
        body = json.loads(latest_requests[2].body)
        assert 'is_active' in body
        assert body['is_active'] is True

    assert settings.is_activated()
