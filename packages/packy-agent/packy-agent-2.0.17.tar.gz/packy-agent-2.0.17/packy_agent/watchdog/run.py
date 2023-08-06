import sys
import signal
import logging

from packy_agent.domain_logic.constants import WATCHDOG_COMPONENT
from packy_agent.watchdog.service import WatchdogService
from packy_agent.configuration.settings import settings
from packy_agent.utils.logging import configure_logging, configure_logging_basic
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.clients.sentry import init_sentry_client
from packy_agent.utils.installation import dump_version, remove_upgrade_in_progress_lock


logger = logging.getLogger(__name__)


def entry():
    settings.set_runtime('component', WATCHDOG_COMPONENT)

    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)
    args = parser.parse_args()

    settings.set_commandline_arguments(vars(args))
    configure_logging_basic(args.log_level)
    init_sentry_client()
    configure_logging(args.log_level)

    remove_upgrade_in_progress_lock()
    dump_version(settings.get_watchdog_version_dump_filename(),
                 settings.get_watchdog_version_dump_variable_name())
    settings.update_started_at_ts()

    service = WatchdogService()
    signal.signal(signal.SIGTERM, lambda signum, frame: service.graceful_stop())
    if settings.is_graceful_exit_on_sigint():
        signal.signal(signal.SIGINT, lambda signum, frame: service.graceful_stop())
    service.run()


if __name__ == '__main__':
    sys.exit(entry())
