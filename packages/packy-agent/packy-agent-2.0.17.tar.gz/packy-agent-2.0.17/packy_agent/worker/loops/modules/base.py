import logging

from packy_agent.exceptions import ImproperlyConfiguredError
from packy_agent.worker.loops.base.scheduled import ScheduledLoop
from packy_agent.worker.loops.base.producer import ProducerLoop


logger = logging.getLogger(__name__)


def get_target(kwargs, module_name):
    target = kwargs.get('target') or kwargs.get('host')
    if not target:
        logger.debug('Target (host) is not configured for %s', module_name)
        return

    return target


def get_packet_size(kwargs, module_name, default=64):
    packet_size = kwargs.get('packet_size')
    if packet_size is None:
        packet_size = default
        logger.warning('Packet size (packet_size) keyword argument was not provided, using '
                       '%s as default (%s)', packet_size, module_name)

    return packet_size


def get_number_of_pings(kwargs, module_name, default=10):
    number_of_pings = kwargs.get('number_of_pings')
    if number_of_pings is None:
        number_of_pings = default
        logger.warning('Number of pings (number_of_pings) keyword argument was not provided, '
                       'using %s as default (%s)', number_of_pings, module_name)

    return number_of_pings


class ScheduledProducerTaskLoop(ProducerLoop, ScheduledLoop):
    loop_type = 'scheduled_producer'
