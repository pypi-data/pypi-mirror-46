import os
import sys

from packy_agent.domain_logic.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.configuration.settings import settings
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging, configure_logging_basic


ACTIVATE_SCRIPT_PATH = '/tmp/packy-activate.sh'
ACTIVATE_PACKY_AGENT_SH = """#!/usr/bin/env bash
source {venv_path}/bin/activate
packy-agent-activate
"""
DEFAULT_LOG_LEVEL = 'ERROR'


def entry():
    configure_logging_basic(DEFAULT_LOG_LEVEL)
    parser = get_base_argument_parser(__loader__.name, default_log_level=DEFAULT_LOG_LEVEL)
    args = parser.parse_args()
    settings.set_commandline_arguments(vars(args))
    configure_logging(DEFAULT_LOG_LEVEL)

    print()
    print('-' * 40)
    print()
    print('Welcome to Packy Agent')
    print()

    if not settings.is_activated():
        with open(ACTIVATE_SCRIPT_PATH, 'w') as f:
            f.write(ACTIVATE_PACKY_AGENT_SH.format(venv_path=os.getenv('VIRTUAL_ENV')))
        os.system(f'chmod u+x {ACTIVATE_SCRIPT_PATH}')

        url = settings.get_console_base_url()
        print(f'Please, activate your Packy Agent at {url} or run `sudo {ACTIVATE_SCRIPT_PATH}`')
        print()


if __name__ == '__main__':
    sys.exit(entry())
