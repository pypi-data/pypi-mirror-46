import logging
import socket
import time

from packy_agent.constants import PING_MODULE, PING_MODULE_LOOP
from packy_agent.domain_logic.modules.ping.base import ping_once
from packy_agent.domain_logic.models.schematics.ping import PingModuleMeasurement
from packy_agent.worker.loops.modules.base import (
    ScheduledProducerTaskLoop, get_target, get_packet_size, get_number_of_pings)

logger = logging.getLogger(__name__)


def ping(*args, **kwargs):

    target = get_target(kwargs, PING_MODULE)
    if not target:
        return

    packet_size = get_packet_size(kwargs, PING_MODULE)
    number_of_pings = get_number_of_pings(kwargs, PING_MODULE)

    interval_ms = kwargs.get('interval_ms')
    if interval_ms is None:
        interval_ms = 0
        logger.warning('Ping interval (interval_ms) keyword argument was not provided, '
                       'using %s as default (ping)', interval_ms)

    measurement = PingModuleMeasurement({
        'target': target,
        'packet_size': packet_size,
        'n_pings': number_of_pings,
        'values': [],
    })  # we place it here because it also saves time moment
    try:
        destination_ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        logger.info('Could not resolve %s to IP address', target)
    else:
        for ping_no in range(1, number_of_pings + 1):
            logger.debug('STARTED %s ping', ping_no)
            start = time.time()
            try:
                rtt_seconds = ping_once(destination_ip_address, 2, packet_size_bytes=packet_size)
                logger.debug('FINISHED %s ping', ping_no)
                if rtt_seconds is None:
                    continue
            except Exception:
                logger.warning('ERROR during ping', exc_info=True)
                continue

            measurement.values_.append(round(rtt_seconds * 1000, 2))

            time_left = interval_ms / 1000. - (time.time() - start)
            if time_left > 0:
                logger.debug(f'WAITING {time_left:.03f} seconds for next ping')
                time.sleep(time_left)

    return measurement


class PingTaskLoop(ScheduledProducerTaskLoop):

    formal_name = PING_MODULE_LOOP

    def __init__(self, schedule, args=(), kwargs=None, outbound_queue=None):
        super().__init__(schedule=schedule, callable_=ping, args=args, kwargs=kwargs,
                         outbound_queue=outbound_queue)
