import logging

from packy_agent.constants import TRACE_MODULE, TRACE_MODULE_LOOP
from packy_agent.domain_logic.modules.traceroute.base import traceroute as traceroute_impl
from packy_agent.domain_logic.modules.traceroute.constants import UDP_METHOD
from packy_agent.worker.loops.modules.base import (
    ScheduledProducerTaskLoop, get_target, get_packet_size, get_number_of_pings)
from packy_agent.domain_logic.models.schematics.traceroute import TraceModuleMeasurement, Hop

HOP_ATTRIBUTES = ('last', 'best', 'worst', 'average', 'stdev')

logger = logging.getLogger(__name__)


def convert_to_hops(traceroute_result, probe_count):
    hops = []
    for x, item in enumerate(traceroute_result):
        hop_primitive = {
            'number': x + 1,

            'reply_number': item.get('reply_hop_number'),
            'ip_address': item.get('host'),

            'loss_abs': item['loss'],
            'sent': probe_count,
        }
        for attr in HOP_ATTRIBUTES:
            value = item.get(attr)
            if value is not None:
                hop_primitive[attr] = round(value * 1000.0, 1)

        hops.append(Hop(hop_primitive, validate=True))

    return hops


def traceroute(*args, **kwargs):
    target = get_target(kwargs, TRACE_MODULE)
    if not target:
        return

    packet_size_bytes = get_packet_size(kwargs, TRACE_MODULE)
    probe_count = get_number_of_pings(kwargs, TRACE_MODULE, default=3)

    measurement = TraceModuleMeasurement({
        'target': target,
        'packet_size': packet_size_bytes,
        'pings': probe_count,
        'hops': [],
    }, validate=True)  # we place it here because it also saves time moment

    if not (28 <= packet_size_bytes <= 1500):
        packet_size_bytes = min(max(28, packet_size_bytes), 1500)
        logger.warning('`packet_size` is out of range from 28 to 1500 (inclusive), '
                       'value is adjusted to {}'.format(packet_size_bytes))

    result = traceroute_impl(target,
                             probe_count=probe_count,
                             packet_size_bytes=packet_size_bytes,
                             max_hops=kwargs.get('ttl', 30),
                             method=kwargs.get('method', UDP_METHOD),
                             max_parallelism=kwargs.get('parallelism', 16))
    if result is None:
        logger.debug('traceroute_impl(%s) returned None', target)
        return

    measurement.hops = convert_to_hops(result, probe_count)
    return measurement


class TracerouteTaskLoop(ScheduledProducerTaskLoop):

    formal_name = TRACE_MODULE_LOOP

    def __init__(self, schedule, args=(), kwargs=None, outbound_queue=None):
        super().__init__(schedule=schedule, callable_=traceroute, args=args, kwargs=kwargs,
                         outbound_queue=outbound_queue)
