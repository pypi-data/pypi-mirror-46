import logging
import math
import select
import socket
from abc import ABCMeta, abstractmethod
import time
from collections import defaultdict

from packy_agent.domain_logic.modules.common.misc import retrieve_ip_and_icmp_packets
from packy_agent.domain_logic.modules.traceroute.constants import ICMP_METHOD, UDP_METHOD
from packy_agent.domain_logic.modules.common.constants import (
    IP_PACKET_HEADER_SIZE_BYTES, ICMP_PACKET_HEADER_SIZE_BYTES, UDP_PACKET_HEADER_SIZE_BYTES)
from packy_agent.domain_logic.modules.common.buffer import (
    buffer_icmp_response, pop_buffered_icmp_response_receive_time)
from packy_agent.domain_logic.modules.traceroute.models import ProbeResult
from packy_agent.exceptions import ImproperlyConfiguredError
from packy_agent.utils.misc import safe_hexlify


MIN_ICMP_METHOD_PACKET_SIZE = IP_PACKET_HEADER_SIZE_BYTES + ICMP_PACKET_HEADER_SIZE_BYTES
MIN_UDP_METHOD_PACKET_SIZE = IP_PACKET_HEADER_SIZE_BYTES + UDP_PACKET_HEADER_SIZE_BYTES
RANGE_MIN = {
    ICMP_METHOD: MIN_ICMP_METHOD_PACKET_SIZE,
    UDP_METHOD: MIN_UDP_METHOD_PACKET_SIZE,
}
MAX_PACKET_SIZE = 1500
MIN_PERIOD_DURATION_SECONDS = 0.001

logger = logging.getLogger(__name__)


class DiscardedReply(Exception):
    pass


def guess_reply_hop_number(ttl):
    if ttl <= 64:
        return 65 - ttl
    elif ttl <= 128:
        return 129 - ttl
    else:
        return 256 - ttl


def aggregate_results(trace_results):
    agg_results = []
    for probe_results in trace_results:
        aggregated = {'loss': probe_results.count(None)}
        filtered_probe_results = list(filter(None, probe_results))
        if filtered_probe_results:
            # TODO(dmu) HIGH: Host may be different for the different probes of the same TTL
            representative_probe = filtered_probe_results[0]
            aggregated['host'] = representative_probe.hop_ip_address
            aggregated['reply_hop_number'] = representative_probe.reply_hop_number
            rtts = tuple(x.rtt_seconds for x in filtered_probe_results)
            aggregated['last'] = rtts[-1]
            aggregated['best'] = min(rtts)
            aggregated['worst'] = max(rtts)
            average = sum(rtts) / len(rtts)
            aggregated['average'] = average

            variance = sum((x - average) ** 2 for x in rtts) / len(rtts)
            aggregated['stdev'] = math.sqrt(variance)

        agg_results.append(aggregated)

    return agg_results


def get_ttl_and_probe_number(max_hops, probe_count):
    for ttl in range(1, max_hops + 1):
        for probe_number in range(probe_count):
            yield (ttl, probe_number)


def does_payload_match(actual_payload, expected_payload):
    payload_len = len(expected_payload)
    if actual_payload:
        actual_payload_len = len(actual_payload)
        if actual_payload_len != payload_len:
            logger.info('Payload length (%s bytes) differ from expected (sent) '
                        'length (%s bytes), but we are forgiving', actual_payload_len, payload_len)
            min_len = min(actual_payload_len, payload_len)
            actual_payload_prefix = actual_payload[:min_len]
            expected_payload_prefix = expected_payload[:min_len]
            if actual_payload_prefix != expected_payload_prefix:
                logger.debug('Payload prefix differs (actual: %s, expected: %s)',
                             safe_hexlify(actual_payload_prefix),
                             safe_hexlify(expected_payload_prefix))
                return False
        elif actual_payload != expected_payload:
            logger.debug('Payload differs (actual: %s, expected: %s)',
                         safe_hexlify(actual_payload), safe_hexlify(expected_payload))
            return False

    return True


class Traceroute(metaclass=ABCMeta):
    range_min = None

    def __init__(self):
        self.sending_socket = None
        self.receiving_socket = None
        # TODO(dmu) HIGH: Take care of memory leak here!
        self.sent_probes = {}

        self.udp_protocol = socket.getprotobyname('udp')
        self.icmp_protocol = socket.getprotobyname('icmp')

    @abstractmethod
    def send_probe(self, probe_number, destination_ip_address, ttl, packet_size_bytes, **kwargs):
        raise NotImplementedError('This method must be implemented in child class')

    @staticmethod
    @abstractmethod
    def is_probe_reply(icmp_packet):
        raise NotImplementedError('This method must be implemented in child class')

    @staticmethod
    @abstractmethod
    def retrieve_probe_packet(icmp_packet):
        raise NotImplementedError('This method must be implemented in child class')

    @abstractmethod
    def process_method_specific_probe_reply(self, ip_packet, icmp_packet, probe_packet):
        raise NotImplementedError('This method must be implemented in child class')

    @staticmethod
    @abstractmethod
    def retrieve_payload(icmp_packet, probe_packet):
        raise NotImplementedError('This method must be implemented in child class')

    @abstractmethod
    def get_sent_probe(self, probe_packet):
        raise NotImplementedError('This method must be implemented in child class')

    @staticmethod
    @abstractmethod
    def is_last_hop(icmp_packet):
        raise NotImplementedError('This method must be implemented in child class')

    @staticmethod
    @abstractmethod
    def get_hop_ip_address(ip_packet, icmp_packet):
        raise NotImplementedError('This method must be implemented in child class')

    def free_resources(self, probe_result):
        pass

    @abstractmethod
    def buffer_icmp_response(self, packet_data, probe_packet, receive_time):
        raise NotImplementedError('This method must be implemented in child class')

    def process_probe_reply(self, data, receive_time):
        logger.debug('PROCESSING probe reply received at %.6f: %s',
                     receive_time, safe_hexlify(data))

        result = retrieve_ip_and_icmp_packets(data)
        if result:
            ip_packet, icmp_packet = result
        else:
            return None, None

        if not self.is_probe_reply(icmp_packet):
            logger.debug('Discarded ICMP packet (reason: not a probe reply) '
                         'from: %s, IP checksum: %s, type: %s, code: %s',
                         ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code)
            return None, None

        probe_packet = self.retrieve_probe_packet(icmp_packet)
        if not probe_packet:
            logger.debug(
                'Discarded ICMP packet (reason: does not contain proper probe packet) '
                'from: %s, IP checksum: %s, type: %s, code: %s',
                ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code)
            return None, None

        if not self.process_method_specific_probe_reply(ip_packet, icmp_packet, probe_packet):
            return probe_packet, None

        probe = self.get_sent_probe(probe_packet)
        assert probe
        expected_payload = probe.payload
        actual_payload = self.retrieve_payload(icmp_packet, probe_packet)
        if not does_payload_match(actual_payload, expected_payload):
            logger.debug('Discarded ICMP packet (reason: payload does not match) '
                         'from: %s, IP checksum: %s, type: %s, code: %s',
                         ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code)
            return probe_packet, None

        logger.debug(
            'Accepted ICMP packet from: %s, IP checksum: %s, type: %s, code: %s, payload: %s',
            ip_packet.src, ip_packet.csum, icmp_packet.type, icmp_packet.code,
            safe_hexlify(actual_payload))

        rtt_seconds = receive_time - probe.sent_time
        return probe_packet, ProbeResult(
            hop_number=probe.ttl,
            reply_hop_number=guess_reply_hop_number(ip_packet.ttl),
            probe_number=probe.probe_number,
            hop_ip_address=self.get_hop_ip_address(ip_packet, icmp_packet),
            rtt_seconds=rtt_seconds,
            is_last_hop=self.is_last_hop(icmp_packet),
            probe=probe)

    def get_probe_result(self):
        logger.debug('Getting probe result...')
        receiving_socket = self.get_receiving_socket()

        ready_sockets = select.select((receiving_socket,), (), (), 0.1)
        # because by this time the entire packet is already in OS buffer
        receive_time = time.time()

        if ready_sockets[0]:
            logger.debug('RECEIVING probe reply from socket...')
            packet_data = receiving_socket.recv(2048)
            logger.debug('RECEIVED data from socket at %.6f: %s',
                         receive_time, safe_hexlify(packet_data))
            probe_packet, probe_result = self.process_probe_reply(packet_data, receive_time)
            if probe_result:
                logger.debug('RECEIVED probe reply from socket: %s', probe_result)
                sent_time = probe_result.probe.sent_time
                assert sent_time <= receive_time, 'Sent after received'

                # Adjust RTT measurement for the case when a parallel greenlet has also received,
                # but earlier
                buffered_receive_time = pop_buffered_icmp_response_receive_time(packet_data)
                if (buffered_receive_time is not None and
                    # There is no better way to tell apart replies of different probes if
                    # they do not contain payload
                        sent_time < buffered_receive_time < receive_time):
                    assert sent_time < buffered_receive_time, 'Sent after buffered receive time'

                    time_delta = receive_time - buffered_receive_time
                    assert time_delta >= 0, 'Packet buffered after it was received'

                    rtt_seconds = probe_result.rtt_seconds - time_delta
                    assert rtt_seconds >= 0, 'RTT is negative'

                    logger.debug('Probe reply has been received %.6f seconds earlier', time_delta)
                    probe_result = ProbeResult(
                        hop_number=probe_result.hop_number,
                        reply_hop_number=probe_result.reply_hop_number,
                        probe_number=probe_result.probe_number,
                        hop_ip_address=probe_result.hop_ip_address,
                        rtt_seconds=rtt_seconds,
                        is_last_hop=probe_result.is_last_hop,
                        probe=probe_result.probe)

                self.free_resources(probe_result)
                return probe_result
            else:
                self.buffer_icmp_response(packet_data, probe_packet, receive_time)
                raise DiscardedReply()
        else:
            logger.debug('NOTHING on socket')

    def do(self, host, timeout=2, probe_count=1, packet_size_bytes=60, max_hops=100,
           max_parallelism=10):
        logger.debug('Starting %s: host=%s, timeout=%s, probe_count=%s, packet_size_bytes=%s, '
                     'max_hops=%s, max_parallelism=%s', self.__class__.__name__, host, timeout,
                     probe_count, packet_size_bytes, max_hops, max_parallelism)
        self.validate_arguments(packet_size_bytes, max_parallelism)
        destination_ip_address = self.get_destination_ip_address(host)
        if not destination_ip_address:
            return

        last_hop_number = max_hops
        results = defaultdict(dict)
        timeout_expiration = None
        active_probes = set()
        is_done = False
        should_send = True
        ttl_and_probe_number_generator = get_ttl_and_probe_number(max_hops, probe_count)
        while not is_done:
            start = time.time()
            if should_send:
                if len(active_probes) < max_parallelism:
                    try:
                        ttl, probe_number = next(ttl_and_probe_number_generator)
                    except StopIteration:
                        logger.debug('Sent out all probes')
                        should_send = False
                    else:
                        should_send = ttl <= last_hop_number
                        if should_send:
                            probe = self.send_probe(probe_number, destination_ip_address, ttl,
                                                    packet_size_bytes)
                            self.sent_probes[probe.key] = probe
                            active_probes.add(probe)
                        else:
                            logger.debug('Last hop has been reached: %s', last_hop_number)
                else:
                    logger.debug('No more room for parallelism')
            else:
                if timeout_expiration is None:
                    timeout_expiration = time.time() + timeout
                logger.debug('No more probes to send')

            while self.sent_probes:
                try:
                    probe_result = self.get_probe_result()
                except DiscardedReply:
                    logger.debug('Nothing on sockets, moving on')
                    if timeout_expiration is not None:
                        timeout_expiration = time.time() + timeout  # Extend timeout
                    break
                else:
                    if probe_result:
                        logger.debug('Got probe result: %s', probe_result)
                        active_probes.discard(probe_result.probe)
                        del self.sent_probes[probe_result.probe.key]
                    else:
                        logger.debug('No probe result yet, moving on')
                        break

                # We got probe result but if does not have hop IP address then it was not sent by the hop
                results[probe_result.hop_number][probe_result.probe_number] = (
                    probe_result if probe_result.hop_ip_address else None)

                if (probe_result.is_last_hop or
                        probe_result.hop_ip_address == destination_ip_address):
                    if probe_result.hop_number < last_hop_number:
                        last_hop_number = probe_result.hop_number
                        logger.debug('CHANGED last hop number to: %s', last_hop_number)

                for ttl_local in range(last_hop_number, 0, -1):
                    results_len = len(results[ttl_local])
                    if results_len < probe_count:
                        logger.debug(
                            'Not all results have arrived yet (only %s replies for TTL: %s)',
                            results_len, ttl_local)
                        break
                else:
                    logger.debug('All results have arrived')
                    is_done = True
                    break

            for active_probe in list(active_probes):
                if time.time() >= active_probe.sent_time + timeout:
                    logger.debug('Probe %s timed out', active_probe)
                    active_probes.discard(active_probe)

            if not should_send and not self.sent_probes:
                logger.debug('No more probes to send or replies to receive')
                break

            if timeout_expiration is not None and time.time() >= timeout_expiration:
                logger.debug('Traceroute timed out')
                break

            duration = time.time() - start
            if duration < MIN_PERIOD_DURATION_SECONDS:
                sleep_duration = MIN_PERIOD_DURATION_SECONDS - duration
                logger.debug('Sleeping for %.6g seconds to stay IO-bound', sleep_duration)
                time.sleep(sleep_duration)

        self.sent_probes.clear()

        # Cut the tail (for unreachable host case)
        new_last_hop_number = last_hop_number
        for ttl in range(last_hop_number, 0, -1):
            new_last_hop_number = ttl
            result = results.get(ttl)
            if result and any(result.values()):
                new_last_hop_number = min(new_last_hop_number + 1, last_hop_number)
                break

        last_hop_number = new_last_hop_number

        return aggregate_results(
            [[results[ttl].get(probe_number) for probe_number in range(probe_count)]
                for ttl in range(1, last_hop_number + 1)])

    @abstractmethod
    def open_sending_socket(self):
        raise NotImplementedError('This method must be implemented in child class')

    def open_receiving_socket(self):
        logger.debug('Opening receiving socket...')
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_RAW, self.icmp_protocol)
        except socket.error as ex:
            if ex.errno == 1:  # Operation not permitted
                # TODO(dmu) HIGH: Fix to receive ICMP packet without being root
                raise socket.error(
                    ex.strerror + '  - process should be running as root.')

            raise

    @staticmethod
    def get_destination_ip_address(host):
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            logger.info('Could not resolve %s to IP address', host)
            return

    def validate_arguments(self, packet_size_bytes, max_parallelism):
        if self.range_min is None:
            raise ImproperlyConfiguredError('`range_min` attribute must be set in child class')

        if max_parallelism < 1:
            raise ValueError('max_parallelism must be greater or equal to 1')

        range_min = self.range_min
        if not (self.range_min <= packet_size_bytes <= MAX_PACKET_SIZE):
            raise ValueError(
                'packet_size_bytes must be in range from {} to 1500 (inclusive)'.format(range_min))

    def get_sending_socket(self):
        self.get_receiving_socket()  # will open receiving socket and make sure no reply is missing
        if not self.sending_socket:
            self.sending_socket = self.open_sending_socket()

        return self.sending_socket

    def get_receiving_socket(self):
        if not self.receiving_socket:
            self.receiving_socket = self.open_receiving_socket()

        return self.receiving_socket

    def close_sending_socket(self):
        if self.sending_socket:
            try:
                self.sending_socket.close()
            except Exception as ex:
                logger.warning('Error while closing sending socket: %r', ex)

            self.sending_socket = None

    def close_receiving_socket(self):
        if self.receiving_socket:
            try:
                self.receiving_socket.close()
            except Exception as ex:
                logger.warning('Error while closing receiving socket: %r', ex)

            self.receiving_socket = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_sending_socket()
        self.close_receiving_socket()


def traceroute(host, timeout=3, probe_count=1, packet_size_bytes=60, max_hops=100,
               method=UDP_METHOD, max_parallelism=10):

    if method not in (UDP_METHOD, ICMP_METHOD):
        raise ValueError('Unknown traceroute method: {}'.format(method))

    if max_parallelism < 1:
        raise ValueError('max_parallelism must be greater or equal to 1')

    range_min = RANGE_MIN[method]
    if not (range_min <= packet_size_bytes <= MAX_PACKET_SIZE):
        raise ValueError(
            'packet_size_bytes must be in range from {} to 1500 (inclusive)'.format(range_min))

    if method == UDP_METHOD:
        from packy_agent.domain_logic.modules.traceroute.methods.udp import TracerouteUDP
        traceroute = TracerouteUDP()
    elif method == ICMP_METHOD:
        from packy_agent.domain_logic.modules.traceroute.methods.icmp import TracerouteICMP
        traceroute = TracerouteICMP()
    else:
        assert False

    with traceroute:
        return traceroute.do(host, timeout=timeout, probe_count=probe_count,
                             packet_size_bytes=packet_size_bytes, max_hops=max_hops,
                             max_parallelism=max_parallelism)
