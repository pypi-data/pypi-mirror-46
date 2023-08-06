from gevent import monkey; monkey.patch_all()

import sys
import signal
import gevent
import logging

from packy_agent.configuration.settings import settings
from packy_agent.utils.logging import configure_logging, configure_logging_basic
from packy_agent.worker.service import Worker
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.clients.sentry import init_sentry_client
from packy_agent.utils.installation import dump_version, remove_upgrade_in_progress_lock
from packy_agent.domain_logic.constants import WORKER_COMPONENT


logger = logging.getLogger(__name__)


def entry():
    settings.set_runtime('component', WORKER_COMPONENT)

    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)
    args = parser.parse_args()

    settings.set_commandline_arguments(vars(args))
    configure_logging_basic(args.log_level)
    init_sentry_client()
    configure_logging(args.log_level)

    remove_upgrade_in_progress_lock()
    dump_version(settings.get_worker_version_dump_filename(),
                 settings.get_worker_version_dump_variable_name())
    settings.update_started_at_ts()

    worker = Worker()

    gevent.signal(signal.SIGTERM, worker.stop)
    if settings.is_graceful_exit_on_sigint():
        gevent.signal(signal.SIGINT, worker.stop)
    worker.run()


if __name__ == '__main__':
    sys.exit(entry())
