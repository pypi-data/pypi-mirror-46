import time
import logging

from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.clients.packy_communication import PackyCommunicationClient
from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.domain_logic.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.configuration.settings import settings
from packy_agent.constants import (COMMUNICATION_LOOP, RELOAD_EVENT, RESTART_EVENT, REBOOT_EVENT,
                                   UPGRADE_EVENT, HEARTBEAT_EVENT)

logger = logging.getLogger(__name__)


class PackyCommunicationLoop(PeriodicLoop):

    formal_name = COMMUNICATION_LOOP

    def __init__(self, period, is_logged_iteration=True, **mkwargs):
        super().__init__(period=period, is_logged_iteration=is_logged_iteration, **mkwargs)

        self.communication_client = None
        self.heartbeat_request_ts = None
        self.heartbeat_received_ts = None

        self.agent_key = settings.get_agent_key()

    def is_communication_timed_out(self):
        if self.heartbeat_request_ts is None:
            return False

        if self.heartbeat_received_ts is None:
            return (time.time() - self.heartbeat_request_ts >
                    settings.get_worker_packy_communication_heartbeat_timeout_seconds())

        return self.heartbeat_received_ts < self.heartbeat_request_ts

    def handle_reload(self, *args, **kwargs):
        # We are restarting everything because some settings are read only once on start and
        # we need to reread them
        logger.info('PROCESSING reload event...')
        control_manager.restart_all()

    def handle_restart(self, *args, **kwargs):
        # We are restarting everything because some settings are read only once on start and
        # we need to reread them
        logger.info('PROCESSING restart event...')
        control_manager.restart_all()

    def handle_reboot(self, *args, **kwargs):
        logger.info('PROCESSING reboot event...')
        control_manager.reboot()

    def handle_upgrade(self, *args, **kwargs):
        logger.info('PROCESSING upgrade event...')
        install_and_upgrade_manager.upgrade_and_restart()

    def handle_heartbeat(self, *args, **kwargs):
        logger.debug(f'PROCESSING heartbeat event ({args}, {kwargs})...')
        self.heartbeat_received_ts = time.time()

    def send_heartbeat(self):
        self.heartbeat_request_ts = self.communication_client.send_heartbeat(self.agent_key)

    def destroy_communication_client(self):
        if self.communication_client:
            self.communication_client.stop()
            self.communication_client = None

        self.heartbeat_request_ts = None
        self.heartbeat_received_ts = None

    def iteration(self):
        if self.communication_client:
            if self.is_communication_timed_out():
                logger.warning('Communication timed out')
                self.destroy_communication_client()
            else:
                self.send_heartbeat()
                return

        if not self.communication_client:  # True after self.destroy_communication_client()
            self.communication_client = PackyCommunicationClient()
            self.communication_client.set_handler(RELOAD_EVENT, self.handle_reload)
            self.communication_client.set_handler(RESTART_EVENT, self.handle_restart)
            self.communication_client.set_handler(REBOOT_EVENT, self.handle_reboot)
            self.communication_client.set_handler(UPGRADE_EVENT, self.handle_upgrade)
            self.communication_client.set_handler(HEARTBEAT_EVENT, self.handle_heartbeat)
            try:
                self.communication_client.start()
            except Exception as ex:
                logger.warning(f'Could not start {self.description}: {ex!r}')
                self.destroy_communication_client()

    def stop(self):
        super().stop()
        self.destroy_communication_client()
