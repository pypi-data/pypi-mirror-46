import logging

import packy_agent
from packy_agent.configuration.settings import settings
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.constants import HEARTBEAT_LOOP
from packy_agent.utils.network import get_actual_ip_address

logger = logging.getLogger(__name__)


class HeartbeatLoop(PeriodicLoop):

    formal_name = HEARTBEAT_LOOP

    def __init__(self, period, *args, **kwargs):
        super().__init__(period, *args, **kwargs)

    def call(self):
        self.collect_log(f'STARTED {self.description} iteration')

        if not settings.is_worker_heartbeat_enabled():
            logger.debug('Heartbeat is disabled')
            return

        try:
            self.collect_log('GETTING actual IP-address...')
            ip_address = get_actual_ip_address()
            self.collect_log(f'GOT actual IP-address: {ip_address}')
            self.collect_log('UPDATING status on Server...')
            get_packy_server_client().update_status(version=packy_agent.__version__,
                                                    ip_address=ip_address)
            self.collect_log('UPDATED status on Server')
        except Exception:
            logger.warning('Error while sending heartbeat', exc_info=True,
                           extra={'iteration_log': list(self.iteration_log)})

        self.collect_log(f'FINISHED {self.description} iteration')
