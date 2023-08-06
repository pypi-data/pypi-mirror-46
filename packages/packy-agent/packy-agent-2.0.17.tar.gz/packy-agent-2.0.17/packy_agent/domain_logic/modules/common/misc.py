import logging

from ryu.lib.packet.icmp import icmp
from ryu.lib.packet.ipv4 import ipv4
from ryu.lib.packet.packet import Packet

from packy_agent.utils.misc import safe_hexlify


logger = logging.getLogger(__name__)


def retrieve_ip_and_icmp_packets(data):
    packet = Packet(data, parse_cls=ipv4)

    protocol_0 = packet.protocols[0]
    if isinstance(protocol_0, ipv4):  # is IP packet?
        ip_packet = protocol_0
        logger.debug('Processing IPv4 packet checksum: %s, from: %s', ip_packet.csum, ip_packet.src)
    else:
        logger.debug('Data is not an IPv4 packet: %s', safe_hexlify(data))
        return

    protocol_1 = packet.protocols[1]
    if isinstance(protocol_1, icmp):
        icmp_packet = protocol_1
        logger.debug('Processing ICMP packet IP checksum: %s, from: %s, type: %s, code: %s',
                     ip_packet.csum, ip_packet.src, icmp_packet.type, icmp_packet.code)
    else:
        logger.debug('Data does not contain an ICMP packet: %s', safe_hexlify(data))
        return

    return ip_packet, icmp_packet
