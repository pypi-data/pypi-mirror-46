import sys


from packy_agent.configuration.settings import settings
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging, configure_logging_basic
from packy_agent.domain_logic.managers.network import network_manager


DEFAULT_LOG_LEVEL = 'ERROR'


def set_dhcp(interface, no_reboot, no_backup):
    kwargs = {'reboot_delay_seconds': None} if no_reboot else {}
    network_manager.set_dhcp(interface, no_backup=no_backup, **kwargs)


def entry():
    configure_logging_basic(DEFAULT_LOG_LEVEL)
    parser = get_base_argument_parser(__loader__.name, default_log_level=DEFAULT_LOG_LEVEL)
    parser.add_argument('-i', '--interface')
    parser.add_argument('--no-reboot', action='store_true')
    parser.add_argument('--no-backup', action='store_true')
    args = parser.parse_args()
    settings.set_commandline_arguments(vars(args))
    configure_logging(DEFAULT_LOG_LEVEL)

    return set_dhcp(args.interface, args.no_reboot, args.no_backup)


if __name__ == '__main__':
    sys.exit(entry())
