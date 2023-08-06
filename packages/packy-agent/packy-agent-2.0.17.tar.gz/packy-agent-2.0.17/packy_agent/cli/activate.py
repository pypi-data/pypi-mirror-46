import logging
import sys
from getpass import getpass

from packy_agent.clients.packy_server import get_inactive_agents
from packy_agent.domain_logic.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.exceptions import AuthenticationError, ValidationError
from packy_agent.configuration.settings import settings
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging, configure_logging_basic


def entry():
    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)

    parser.add_argument('--email')
    parser.add_argument('--password')

    args = parser.parse_args()
    settings.set_commandline_arguments(vars(args))
    configure_logging(logging.WARNING)

    if settings.is_activated():
        print('Packy Agent is already activated')
        return 1

    print('Packy Agent activation')

    email = args.email or input('E-mail: ')
    password = args.password or getpass('Password: ')

    try:
        agents = get_inactive_agents(email, password)
        activating_agent_id = None
        if agents:
            print('Activate as:')
            print('[enter] New agent')
            for agent_id, agent_name in agents.items():
                print(f'[id={agent_id}] {agent_name}')

            while True:
                agent_id = input('Agent id: ') or None
                if agent_id:
                    try:
                        activating_agent_id = int(agent_id)
                    except (ValueError, TypeError):
                        print('Agent ID must be an integer')
                    else:
                        break
                else:
                    break

        install_and_upgrade_manager.activate(email, password, agent_id=activating_agent_id)
    except AuthenticationError:
        print('Not authenticated (invalid credentials)')
        return 1
    except ValidationError as ex:
        print(f'Validation error: {ex}')
        return 1

    print()
    print('-------------------------------------')
    print('Packy Agent is activated successfully')
    print()


if __name__ == '__main__':
    sys.exit(entry())
