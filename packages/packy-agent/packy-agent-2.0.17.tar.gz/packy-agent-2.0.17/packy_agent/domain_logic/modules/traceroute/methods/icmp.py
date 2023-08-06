import logging
import socket
import os

import gevent
from ryu.lib.packet.icmp import icmp, ICMP_ECHO_REPLY, ICMP_TIME_EXCEEDED, ICMP_DEST_UNREACH
from ryu.lib.packet.ipv4 import ipv4
from ryu.lib.packet.packet import Packet

from packy_agent.domain_logic.modules.common.socket import (
    get_seq_no, send_icmp_echo_request as send_icmp_probe, ICMP_PROTOCOL)
from packy_agent.domain_logic.modules.traceroute.base import Traceroute
from packy_agent.domain_logic.modules.traceroute.models import SentProbe
from packy_agent.domain_logic.modules.common.constants import (IP_PACKET_HEADER_SIZE_BYTES,
                                                               ICMP_PACKET_HEADER_SIZE_BYTES)
from packy_agent.utils.misc import safe_hexlify
from packy_agent.domain_logic.modules.common.buffer import buffer_icmp_response


PACKET_HEADERS_SIZE_BYTES = IP_PACKET_HEADER_SIZE_BYTES + ICMP_PACKET_HEADER_SIZE_BYTES

logger = logging.getLogger(__name__)


def get_icmp_id():
    return (os.getpid() + id(gevent.getcurrent())) & 0xFFFF


class TracerouteICMP(Traceroute):

    range_min = PACKET_HEADERS_SIZE_BYTES

    def send_probe(self, probe_number, destination_ip_address, ttl, packet_size_bytes=60, **kwargs):
        sending_socket = self.get_sending_socket()
        sending_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        seq_no = get_seq_no(ICMP_PROTOCOL)
        sent_time, sent_payload = send_icmp_probe(
            sending_socket, destination_ip_address, get_icmp_id(), seq_no,
            payload_size_bytes=packet_size_bytes - PACKET_HEADERS_SIZE_BYTES, **kwargs)
        return SentProbe(ttl, probe_number, sent_time, sent_payload, seq_no)

    @staticmethod
    def is_probe_reply(icmp_packet):
        return icmp_packet.type in (ICMP_TIME_EXCEEDED, ICMP_ECHO_REPLY, ICMP_DEST_UNREACH)

    @staticmethod
    def retrieve_probe_packet(icmp_packet):
        if icmp_packet.type in (ICMP_TIME_EXCEEDED, ICMP_DEST_UNREACH):
            inner_packet = Packet(icmp_packet.data.data, parse_cls=ipv4)
            protocol_1 = inner_packet.protocols[1]
            if isinstance(protocol_1, icmp):
                effective_icmp_packet = protocol_1
            else:
                logger.debug('ICMP packet does not contain inner ICMP packet')
                return
        elif icmp_packet.type == ICMP_ECHO_REPLY:
            effective_icmp_packet = icmp_packet
        else:
            raise ValueError(f'Unsupported ICMP packet type: {icmp_packet.type}')

        logger.debug(
            'Processing ICMP packet id:%s, seq:%s, payload:%s', effective_icmp_packet.data.id,
            effective_icmp_packet.data.seq, safe_hexlify(effective_icmp_packet.data.data))

        return effective_icmp_packet

    def process_method_specific_probe_reply(self, ip_packet, icmp_packet, probe_packet):
        id_ = probe_packet.data.id
        if id_ != get_icmp_id():
            logger.debug('Discarded ICMP packet (reason: unexpected id %s) '
                         'from: %s, IP checksum: %s, type: %s, code: %s',
                         probe_packet.data.id,
                         ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code)
            return False

        seq = probe_packet.data.seq
        if seq not in self.sent_probes:
            logger.debug('Discarded ICMP packet (reason: unexpected seq %s) '
                         'from: %s, IP checksum: %s, type: %s, code: %s', seq,
                         ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code)
            return False

        return True

    @staticmethod
    def retrieve_payload(icmp_packet, probe_packet):
        return probe_packet.data.data

    def get_sent_probe(self, probe_packet):
        return self.sent_probes.get(probe_packet.data.seq)

    @staticmethod
    def is_last_hop(icmp_packet):
        if icmp_packet.type == ICMP_TIME_EXCEEDED:
            return False
        elif icmp_packet.type in (ICMP_ECHO_REPLY, ICMP_DEST_UNREACH):
            return True
        else:
            raise ValueError(
                f'Unsupported ICMP packet type: {icmp_packet.type} (should never get here)')

    @staticmethod
    def get_hop_ip_address(ip_packet, icmp_packet):
        return None if icmp_packet.type == ICMP_DEST_UNREACH else ip_packet.src

    def buffer_icmp_response(self, packet_data, probe_packet, receive_time):
        buffer_icmp_response(packet_data, receive_time)

    def open_sending_socket(self):
        logger.debug('Opening sending socket...')
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_RAW, self.icmp_protocol)
        except socket.error as ex:
            if ex.errno == 1:  # Operation not permitted
                # TODO(dmu) HIGH: Fix to receive ICMP packet without being root
                raise socket.error(
                    ex.strerror + '  - process should be running as root.')

            raise

    def get_sending_socket(self):
        if not self.sending_socket:
            self.sending_socket = self.receiving_socket or self.open_sending_socket()

        return self.sending_socket

    def get_receiving_socket(self):
        if not self.receiving_socket:
            self.receiving_socket = self.sending_socket or self.open_receiving_socket()

        return self.receiving_socket
