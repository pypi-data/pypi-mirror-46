import socket
import time
import logging
import random

import cachetools
from ryu.lib.packet.ipv4 import ipv4
from ryu.lib.packet.udp import udp
from ryu.lib.packet.icmp import ICMP_TIME_EXCEEDED, ICMP_DEST_UNREACH, ICMP_PORT_UNREACH_CODE
from ryu.lib.packet.packet import Packet

from packy_agent.domain_logic.modules.traceroute.base import Traceroute
from packy_agent.domain_logic.modules.traceroute.models import SentProbe
from packy_agent.domain_logic.modules.common.socket import (
    TIME_SIZE_BYTES, encode_timestamp)
from packy_agent.domain_logic.modules.common.constants import (
    IP_PACKET_HEADER_SIZE_BYTES, UDP_PACKET_HEADER_SIZE_BYTES)
from packy_agent.utils.misc import generate_random_string, safe_hexlify
from packy_agent.exceptions import OutOfPortsError
from packy_agent.domain_logic.modules.common.buffer import buffer_icmp_response


PACKET_HEADERS_SIZE_BYTES = IP_PACKET_HEADER_SIZE_BYTES + UDP_PACKET_HEADER_SIZE_BYTES
UDP_PORT_LOW = 33434
UDP_PORT_HIGH = 35357 - 1  # `OpenStack Identity (Keystone) administration` minus one
# These ports are unofficially assigned to Jenkins, Infestation: Survivor Stories, Factorio
UDP_PORT_GAPS = (33848, 34000, 34197)  # these ports are uno

TTL_CACHE_SIZE = UDP_PORT_HIGH - UDP_PORT_LOW - len(UDP_PORT_GAPS) + 1
used_udp_ports = cachetools.TTLCache(TTL_CACHE_SIZE, ttl=60)
used_udp_ports[UDP_PORT_LOW] = None


logger = logging.getLogger(__name__)


def reserve_udp_port():
    while True:
        used_udp_ports_len = len(used_udp_ports)
        if used_udp_ports_len >= TTL_CACHE_SIZE:
            raise OutOfPortsError()

        # It appears that using higher port numbers produce strange results therefore using this
        # formula use lower port number if possible
        # Widen the range to reduce probability of wrong buffered receive time issue
        high = min(max(UDP_PORT_LOW + (used_udp_ports_len * 2) + 1, UDP_PORT_LOW + 200),
                   UDP_PORT_HIGH + 1)
        port = random.randrange(UDP_PORT_LOW, high, 1)
        if port in used_udp_ports or port in UDP_PORT_GAPS:
            time.sleep(0.001)
            continue

        used_udp_ports[port] = None
        logger.debug('RESERVED UDP port: %s', port)
        return port


def free_udp_port(port):
    logger.debug('FREED UDP port: %s', port)
    used_udp_ports.pop(port, None)


def send_udp_probe(raw_socket, destination_ip_address, port, ttl, packet_size_bytes=60,
                   payload=None):
    logger.debug('Sending probe UDP packet to %s:%s (TTL:%s)...', destination_ip_address, port, ttl)
    raw_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    sent_time = time.time()
    time_part = encode_timestamp(sent_time)
    if payload is None:
        if packet_size_bytes < PACKET_HEADERS_SIZE_BYTES:
            raise ValueError('payload_size_bytes must be greater or equal to {}'.format(
                PACKET_HEADERS_SIZE_BYTES))

        payload_size_bytes = packet_size_bytes - PACKET_HEADERS_SIZE_BYTES

        if payload_size_bytes < TIME_SIZE_BYTES:
            payload = generate_random_string(payload_size_bytes).encode('ascii')
        else:
            payload = time_part + generate_random_string(
                payload_size_bytes - TIME_SIZE_BYTES).encode('ascii')
    else:
        payload = time_part + payload

    raw_socket.sendto(payload, (destination_ip_address, port))
    logger.debug('Sent UDP packet to {}:{} (TTL:{}), payload: {}'.format(
        destination_ip_address, port, ttl, safe_hexlify(payload)))
    return sent_time, payload


class TracerouteUDP(Traceroute):

    range_min = PACKET_HEADERS_SIZE_BYTES

    def send_probe(self, probe_number, destination_ip_address, ttl, packet_size_bytes=60, **kwargs):
        port = reserve_udp_port()
        sent_time, sent_payload = send_udp_probe(
            self.get_sending_socket(), destination_ip_address=destination_ip_address,
            port=port, ttl=ttl, packet_size_bytes=packet_size_bytes)
        return SentProbe(ttl, probe_number, sent_time, sent_payload, port)

    @staticmethod
    def is_probe_reply(icmp_packet):
        return icmp_packet.type in (ICMP_TIME_EXCEEDED, ICMP_DEST_UNREACH)

    @staticmethod
    def retrieve_probe_packet(icmp_packet):
        inner_packet = Packet(icmp_packet.data.data, parse_cls=ipv4)
        protocol_1 = inner_packet.protocols[1]
        if isinstance(protocol_1, udp):
            udp_packet = protocol_1
            logger.debug('Processing UDP packet port: %s', udp_packet.dst_port)
            return udp_packet
        else:
            logger.debug('ICMP packet does not contain a UDP packet')
            return

    def process_method_specific_probe_reply(self, ip_packet, icmp_packet, probe_packet):
        probe_port = probe_packet.dst_port
        if probe_port not in self.sent_probes:
            logger.debug('Discarded ICMP packet (reason: unexpected port %s) '
                         'from: %s, IP checksum: %s, type: %s, code: %s', probe_port,
                         ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code)
            return False

        return True

    @staticmethod
    def retrieve_payload(icmp_packet, probe_packet):
        inner_packet = Packet(icmp_packet.data.data, parse_cls=ipv4)
        if len(inner_packet.protocols) > 2:
            # TODO(dmu) HIGH: Is it possible to retrieve payload from udp_packet?
            return inner_packet.protocols[2]

    def get_sent_probe(self, probe_packet):
        return self.sent_probes.get(probe_packet.dst_port)

    @staticmethod
    def is_last_hop(icmp_packet):
        if icmp_packet.type == ICMP_TIME_EXCEEDED:
            return False
        elif icmp_packet.type == ICMP_DEST_UNREACH:
            # weird, but it means that destination is reached if we get a destination unreachable
            # ICMP packet with code ICMP_PORT_UNREACH_CODE
            return True
        else:
            raise ValueError(
                f'Unsupported ICMP packet type: {icmp_packet.type} (should never get here)')

    @staticmethod
    def get_hop_ip_address(ip_packet, icmp_packet):
        if icmp_packet.type == ICMP_DEST_UNREACH and icmp_packet.code != ICMP_PORT_UNREACH_CODE:
            return
        else:
            return ip_packet.src

    def buffer_icmp_response(self, packet_data, probe_packet, receive_time):
        # Buffering must be done only if there is a greenlet waiting for the packet, otherwise
        # we get issues (bug) because of receiving the same reply without payload
        # (so they are exactly the same) for wrong greenlet:
        # 1. Greenlet 1 sends to UDP port 33439
        # 2. Greentet 1 receives reply for port 33439 and frees the port
        # 3. Greenlet 2 receives reply for port 33439, but buffers it, since it is for Greenlet 1 (
        #    (but Greenlet 1 will not remove it from buffer, since it is already done with port
        #     33439)
        # 4. Greenlet 3 reuses port 33439 and sends UDP probe
        # 5. Greenlet 3 receives reply for port 33439, but also gets receive time from buffered
        #    by Greenlet 2 reply (which happens to be before UDP probe was sent)
        # 6. Greenlet 3 calculates negative RTT
        # There is a tiny moment when a port is already reserved, but pocket is not actually sent
        # yet. To protect from it we also check the probe is saved as sent (this may introduce
        # measurement inaccuracy, which considered to be negligible)
        # TODO(dmu) HIGH: It still can get response for a wrong probe which will result in the
        #                 wrong measurement. Need to investigate if there is a theoretical
        #                 possibility to avoid this keeping parallel traceroutes
        if probe_packet:
            port = probe_packet.dst_port
            if port in used_udp_ports and port in self.sent_probes:
                return

        buffer_icmp_response(packet_data, receive_time)

    def free_resources(self, probe_result):
        free_udp_port(probe_result.probe.key)

    def open_sending_socket(self):
        logger.debug('Opening sending socket...')
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, self.udp_protocol)
        except socket.error as ex:
            if ex.errno == 1:  # Operation not permitted
                # TODO(dmu) HIGH: Fix to receive ICMP packet without being root
                raise socket.error(
                    ex.strerror + '  - process should be running as root.')

            raise
