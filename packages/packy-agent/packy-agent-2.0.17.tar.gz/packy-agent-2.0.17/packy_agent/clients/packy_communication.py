import logging
import time

import certifi
from wampy.peers.clients import Client, WampyError

from packy_agent.utils.wampy import TicketMessageHandler, CustomWebSocket, CustomSecureWebSocket
from packy_agent.configuration.settings import settings
from packy_agent.constants import HEARTBEAT_EVENT

TOPIC_TEMPLATE = 'agent.{event}.{agent_key}'
HEARTBEAT_OPTIONS = {'exclude_me': False}


logger = logging.getLogger(__name__)


class PackyCommunicationClient(Client):

    def __init__(self):
        roles = settings.get_communication_roles()
        url = settings.get_communication_url()

        ticket = settings.get_access_token()
        message_handler = TicketMessageHandler(ticket)

        super().__init__(url=url, roles=roles, message_handler=message_handler,
                         cert_path=certifi.where())

        # TODO(dmu) HIGH: Remove this once https://github.com/noisyboiler/wampy/pull/70/files
        #                 is released
        if self.router.scheme == 'ws':
            self.transport = CustomWebSocket(server_url=self.router.url, ipv=self.router.ipv)
        elif self.router.scheme == 'wss':
            self.transport = CustomSecureWebSocket(
                server_url=self.router.url, ipv=self.router.ipv,
                certificate_path=self.router.certificate)
        else:
            raise WampyError('Network protocol must be "ws" or "wss"')

        self.has_registered_roles = False
        self.handlers = {}

    def set_handler(self, event, handler):
        self.handlers[event] = handler

    def register_roles(self):
        super().register_roles()

        agent_key = settings.get_agent_key()

        for event, handler in self.handlers.items():
            topic = TOPIC_TEMPLATE.format(event=event, agent_key=agent_key)
            self.session._subscribe_to_topic(handler, topic)
            logger.debug("%s subscribed to topic '%s'", self.name, topic)

        self.has_registered_roles = True

    def send_heartbeat(self, agent_key):
        request_ts = time.time()
        self.publish(
            topic=TOPIC_TEMPLATE.format(event=HEARTBEAT_EVENT, agent_key=agent_key),
            message={'request_ts': request_ts},
            options=HEARTBEAT_OPTIONS)

        return request_ts
