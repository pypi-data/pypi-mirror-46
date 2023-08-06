import os
import sys
import logging

import yaml

from packy_agent.configuration.settings import settings
from packy_agent.configuration.sources.defaults_dict import defaults
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging_basic
from packy_agent.domain_logic.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.clients.packy_server import get_packy_server_client


# Use as least as possible from rest of the package because it will run at partially
# installed stage


DEFAULT_LOG_LEVEL = 'INFO'

AGENT_CONFIG_ENVVAR_NAME = 'PACKY_AGENT_CONFIG'
DEFAULT_AGENT_CONFIG_PATH = '/etc/packy-agent.yaml'
CONTROL_SERVER_CONFIG_ENVVAR_NAME = 'PACKY_CONTROL_SERVER_CONFIG'
DEFAULT_CONTROL_SERVER_CONFIG_PATH = '/etc/packy-control-server.yaml'


logger = logging.getLogger(__name__)


def read_control_server_configuration():
    control_server_config_filename = os.getenv(
                CONTROL_SERVER_CONFIG_ENVVAR_NAME, DEFAULT_CONTROL_SERVER_CONFIG_PATH)
    logger.info('Reading Control Server configuration file: %s', control_server_config_filename)
    try:
        with open(control_server_config_filename) as f:
            return yaml.load(f)
    except FileNotFoundError:
        logger.info('Control Server configuration file was not found: %s',
                    control_server_config_filename)
        return


def migrate_console_http_port(control_server_config):
    http_port = ((control_server_config.get('packy') or {}).get('control_server') or {}
                 ).get('http_port')
    if http_port is not None:
        settings_filename = os.getenv('PACKY_AGENT_SETTINGS_FILENAME',
                                      defaults['settings_filename'])
        with open(settings_filename) as f:
            settings_file = yaml.load(f)
            settings_file['console'] = settings_file.get('console') or {}
            settings_file['console']['http_port'] = http_port

        with open(settings_filename, 'w') as f:
            yaml.dump(settings_file, f, default_flow_style=False)


def migrate_flask_secret_key(control_server_config):
    secret_key = (control_server_config.get('flask') or {}).get('SECRET_KEY')
    if secret_key:
        settings.set_console_flask_secret_key(secret_key)


def read_agent_configuration():
    agent_config_filename = os.getenv(AGENT_CONFIG_ENVVAR_NAME, DEFAULT_AGENT_CONFIG_PATH)
    logger.info('Reading Agent configuration file: %s', agent_config_filename)

    try:
        with open(agent_config_filename) as f:
            return yaml.load(f)
    except FileNotFoundError:
        logger.info('Agent configuration file was not found: %s', agent_config_filename)
        return


def migrate_activation_status(agent_configuration):
    inner_config = (agent_configuration.get('packy') or {}).get('agent')
    if not inner_config:
        logger.info('packy.agent key is not found, maybe agent was not activated')
        return

    agent_id = inner_config.get('agent_id')
    if agent_id is None:
        logger.warning('agent_id was not found or empty')
        return

    client_id = inner_config.get('client_id')
    if client_id is None:
        logger.warning('client_id was not found or empty')
        return

    client_secret = inner_config.get('client_secret')
    if client_secret is None:
        logger.warning('client_secret was not found or empty')
        return

    temp_access_token = get_packy_server_client().get_access_token_for_credentials(client_id,
                                                                             client_secret)
    get_packy_server_client().deactivate_agent_legacy(temp_access_token, agent_id)
    install_and_upgrade_manager.activate(access_token=temp_access_token, agent_id=agent_id,
                                         ensure_restarted=False)


def migrate():
    control_server_configuration = read_control_server_configuration()
    if control_server_configuration:
        migrate_console_http_port(control_server_configuration)
        migrate_flask_secret_key(control_server_configuration)

    agent_configuration = read_agent_configuration()
    if agent_configuration:
        migrate_activation_status(agent_configuration)


def entry():
    configure_logging_basic(DEFAULT_LOG_LEVEL)
    parser = get_base_argument_parser(__loader__.name, default_log_level=DEFAULT_LOG_LEVEL)
    args = parser.parse_args()
    configure_logging_basic(args.log_level)

    return migrate()


if __name__ == '__main__':
    sys.exit(entry())
