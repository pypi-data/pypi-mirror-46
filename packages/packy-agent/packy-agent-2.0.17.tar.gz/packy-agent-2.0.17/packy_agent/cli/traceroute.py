import logging
import sys

from tabulate import tabulate

from packy_agent.configuration.settings import settings
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging, configure_logging_basic
from packy_agent.domain_logic.modules.traceroute import base
from packy_agent.domain_logic.modules.traceroute.constants import TRACEROUTE_METHODS, UDP_METHOD


def do_traceroute(host, timeout=3, probe_count=1, packet_size_bytes=60, max_hops=30,
                  method=UDP_METHOD, max_parallelism=1):
    agg_results = base.traceroute(host, timeout=timeout, probe_count=probe_count,
                                  packet_size_bytes=packet_size_bytes, max_hops=max_hops,
                                  method=method, max_parallelism=max_parallelism)
    if not agg_results:
        print('No results')
        return

    headers = ['#', 'target', 'average']
    for agg_result in agg_results:
        headers.extend(agg_result.keys() - set(headers) - {'host'})

    rows = [
        [x, result.get('host')] + [result.get(k) for k in headers[2:]] for x, result in
        enumerate(agg_results, start=1)]

    print(tabulate(rows, headers=headers, tablefmt='orgtbl'))


def entry():
    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)

    parser.add_argument('host')
    parser.add_argument('--max-hops', help='max hops', type=int, default=30)
    parser.add_argument('--probe-count', help='probe count', type=int, default=3)
    parser.add_argument('--packet-size-bytes', help='IP packet size in bytes',
                        type=int, default=60)
    parser.add_argument('--max-parallelism', help='max parallelism', type=int, default=1)
    parser.add_argument('--timeout', help='timeout', type=float, default=3)
    parser.add_argument('-M', '--method', help='method', choices=TRACEROUTE_METHODS,
                        default=UDP_METHOD)

    args = parser.parse_args()
    settings.set_commandline_arguments(vars(args))
    configure_logging(logging.WARNING)

    return do_traceroute(args.host, timeout=args.timeout, probe_count=args.probe_count,
                         packet_size_bytes=args.packet_size_bytes,
                         max_hops=args.max_hops, method=args.method,
                         max_parallelism=args.max_parallelism)


if __name__ == '__main__':
    sys.exit(entry())
