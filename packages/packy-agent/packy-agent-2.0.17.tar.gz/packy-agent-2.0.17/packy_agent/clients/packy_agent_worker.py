import logging
from urllib.parse import urljoin

import requests

from packy_agent.configuration.settings import settings
from packy_agent.utils.container import container


logger = logging.getLogger(__name__)


class PackyAgentWorkerClient:

    def get_base_url(self):
        return 'http://{}:{}'.format(settings.get_worker_http_bind_address(),
                                     settings.get_worker_http_port())

    def get_status(self):
        url = urljoin(self.get_base_url(), '/status/')
        logger.debug('Getting Worker status at %s', url)

        response = requests.get(url)
        response.raise_for_status()
        return response.json()


def get_packy_agent_worker_client():
    client = getattr(container, 'packy_agent_worker_client', None)
    if not client:
        container.packy_agent_worker_client = client = PackyAgentWorkerClient()

    return client
