import logging
import os
import socket
import select
import time

from ryu.lib.packet.icmp import ICMP_ECHO_REPLY

from contextlib import closing
from packy_agent.domain_logic.modules.common.socket import (
    get_seq_no, TIME_SIZE_BYTES, send_icmp_echo_request, decode_timestamp)
from packy_agent.domain_logic.modules.common.buffer import (
    pop_buffered_icmp_response_receive_time, buffer_icmp_response)
from packy_agent.domain_logic.modules.common.misc import retrieve_ip_and_icmp_packets


logger = logging.getLogger(__name__)


def process_probe_reply(packet_data, seq_no, id_, expected_payload):
    result = retrieve_ip_and_icmp_packets(packet_data)
    if result:
        ip_packet, icmp_packet = result
    else:
        return

    ip_address = ip_packet.src

    logger.debug('Got ICMP packet type:%s code:%s from %s',
                 icmp_packet.type, icmp_packet.code, ip_address)
    if icmp_packet.type != ICMP_ECHO_REPLY:
        logger.debug('Discarded ICMP packet type:{} code:{} from {}'.format(
            icmp_packet.type, icmp_packet.code, ip_address))
        return

    packet_seq = icmp_packet.data.seq
    packet_id = icmp_packet.data.id
    packet_payload = icmp_packet.data.data
    expected_payload_len = len(expected_payload)

    logger.debug(
        'ICMP packet from {} type:{} code:{} has id:{}, seq:{}, payload:{}'.format(
            ip_address, icmp_packet.type, icmp_packet.code, packet_id, packet_seq,
            packet_payload.hex() if packet_payload else packet_payload))

    if packet_seq != seq_no or packet_id != id_:
        return

    if packet_payload:
        packet_payload_len = len(packet_payload)
        if packet_payload_len != expected_payload_len:
            logger.info('Received payload length (%s bytes) differ from expected (sent) '
                        'length (%s bytes), but we are forgiving', packet_payload_len,
                        expected_payload_len)
            min_len = min(packet_payload_len, expected_payload_len)
            if packet_payload[:min_len] != expected_payload[:min_len]:
                logger.debug('Discarded ICMP packet type:{} code:{} from {}: '
                             'payload prefix differs'.format(icmp_packet.type,
                                                             icmp_packet.code, ip_address))
                return
        elif packet_payload != expected_payload:
            logger.debug('Discarded ICMP packet type:{} code:{} from {}: '
                         'payload differs'.format(icmp_packet.type, icmp_packet.code,
                                                  ip_address))
            return

    return packet_payload


def receive_icmp_reply(raw_socket, id_, seq_no, expected_payload, timeout, sent_time):
    expected_payload_len = len(expected_payload)

    time_left = timeout
    while time_left > 0:
        start_time = time.time()
        ready_sockets = select.select((raw_socket,), (), (), time_left)
        receive_time = time.time()  # because by this time the entire packet is already in OS buffer

        if not ready_sockets[0]:  # socket timeout
            break

        time_left -= (receive_time - start_time)

        packet_data, (ip_address, _) = raw_socket.recvfrom(1024 + expected_payload_len)
        packet_payload = process_probe_reply(packet_data, seq_no, id_, expected_payload)
        if packet_payload is None:
            buffer_icmp_response(packet_data, receive_time)
            continue

        if packet_payload and len(packet_payload) >= TIME_SIZE_BYTES:
            sent_time = decode_timestamp(packet_payload[:TIME_SIZE_BYTES])

        buffered_receive_time = pop_buffered_icmp_response_receive_time(packet_data)
        if buffered_receive_time is not None:
            return buffered_receive_time - sent_time
        else:
            return receive_time - sent_time


def ping_once(destination_ip_address, timeout, packet_size_bytes=56):
    icmp_protocol = socket.getprotobyname('icmp')
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_protocol)) as raw_socket:
            id_ = os.getpid() & 0xFFFF
            seq_no = get_seq_no('icmp')
            sent_time, payload = send_icmp_echo_request(
                raw_socket, destination_ip_address, id_, seq_no, packet_size_bytes)
            return receive_icmp_reply(raw_socket, id_, seq_no, payload, timeout,
                                      sent_time=sent_time)

    except OSError as ex:
        if ex.errno == 1:  # Operation not permitted
            # TODO(dmu) HIGH: Allow not root pings
            raise OSError(ex.strerror +
                          ' - Note that ICMP messages can only be sent from processes '
                          'running as root.')

        raise
