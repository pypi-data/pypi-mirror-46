import time
import logging

from packy_agent.worker.loops.main import MainLoop
from packy_agent.configuration.settings import settings
from packy_agent.clients.packy_server import get_packy_server_client


logger = logging.getLogger(__name__)


class Worker:

    def __init__(self):
        self.main_loop = None

    def run(self):
        logger.info('STARTED worker')
        if not settings.is_activated():
            logger.info('WAITING for agent activation...')

            activation_notify_period_seconds = settings.get_worker_activation_notify_period_seconds()
            while not settings.is_activated():
                get_packy_server_client().notify_server(settings.get_console_base_url())
                time.sleep(activation_notify_period_seconds)

        if settings.is_worker_stopped():
            logger.info('WAITING worker to be started...')

            started_check_period_seconds = settings.get_worker_started_check_period_seconds()
            while settings.is_worker_stopped():
                time.sleep(started_check_period_seconds)

        self.main_loop = MainLoop()
        self.main_loop.run()

        logger.info('STOPPED worker')

    def stop(self):
        logger.info('STOP requested for worker')
        if self.main_loop:
            self.main_loop.stop()
