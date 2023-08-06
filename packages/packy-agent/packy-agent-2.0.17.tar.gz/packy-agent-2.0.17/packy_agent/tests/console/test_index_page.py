import pytest

from urllib.parse import urlparse


def test_index_page_smoke(console_flask_client):
    response = console_flask_client.get('/')
    assert response.status_code == 302
    assert urlparse(response.location).path == '/activate/'


@pytest.mark.usefixtures('activated')
def test_index_page_activated_agent(console_flask_client):
    response = console_flask_client.get('/')
    assert response.status_code == 302
    assert urlparse(response.location).path == '/login/'
