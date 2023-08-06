import logging

import cachetools

from packy_agent.utils.misc import safe_hexlify


PACKETS_CACHE_SIZE = 1000

logger = logging.getLogger(__name__)
icmp_responses = cachetools.TTLCache(PACKETS_CACHE_SIZE, ttl=60)


def buffer_icmp_response(data, receive_time):
    hexlified = safe_hexlify(data)
    logger.debug('Buffering ICMP response received at %.6f data: %s', receive_time, hexlified)

    if data in icmp_responses:
        logger.debug('ICMP response is already buffered at %.6f: %s',
                     icmp_responses.get(data), hexlified)
        return

    icmp_responses[data] = receive_time


def pop_buffered_icmp_response_receive_time(data):
    return icmp_responses.pop(data, None)


def is_non_empty_icmp_responses_buffer():
    return bool(icmp_responses)


def iter_icmp_responses():
    for data, receive_time in icmp_responses.items():
        yield data, receive_time


def remove_icmp_response_from_buffer(data):
    hexlified = safe_hexlify(data)
    logger.debug('REMOVING ICMP response: %s', hexlified)
    removed = icmp_responses.pop(data, None)
    if removed:
        logger.debug('REMOVED ICMP response: %s', hexlified)
    else:
        logger.debug('ICMP response was not found in buffer: %s', hexlified)
