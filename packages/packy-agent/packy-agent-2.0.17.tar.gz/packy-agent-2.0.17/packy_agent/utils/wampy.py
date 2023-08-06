import logging
import socket

from wampy.message_handler import MessageHandler
from wampy.transports.websocket.connection import WebSocket, SecureWebSocket


logger = logging.getLogger(__name__)


class TicketAuthenticate:
    WAMP_CODE = 5
    name = 'authenticate'

    def __init__(self, ticket, kwargs_dict=None):
        super(TicketAuthenticate, self).__init__()

        self.ticket = ticket
        self.kwargs_dict = kwargs_dict or {}

    @property
    def message(self):
        return [self.WAMP_CODE, self.ticket, self.kwargs_dict]


class TicketMessageHandler(MessageHandler):

    ticket = None

    def __init__(self, ticket) -> None:
        super().__init__()
        self.ticket = ticket

    def handle_challenge(self, message_obj):
        logger.debug('client has been Challenged')
        message = TicketAuthenticate(self.ticket)
        self.session.send_message(message)


class CustomWebSocket(WebSocket):
    def disconnect(self):
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass

            self.socket.close()


class CustomSecureWebSocket(SecureWebSocket, CustomWebSocket):
    pass
