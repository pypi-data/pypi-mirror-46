import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

import packy_agent
from packy_agent.utils.platforms import get_platform
from packy_agent.configuration.settings import settings

logger = logging.getLogger(__name__)


def init_sentry_client(log_level=None, flask_integration=False, packy_agent_sentry_dsn=None, **kwargs):
    if not packy_agent_sentry_dsn:
        packy_agent_sentry_dsn = settings.get_sentry_dsn()

    if packy_agent_sentry_dsn:
        component = settings.get_component()
        platform_name = get_platform()
        release = f'Packy Agent v{packy_agent.__version__} / {component} / {platform_name}'

        if log_level is None:
            log_level = settings.get_current_component_setting('sentry_log_level', logging.ERROR)

        integrations = [LoggingIntegration(level=log_level, event_level=log_level)]
        if flask_integration:
            integrations.append(FlaskIntegration())

        agent_key = settings.get_agent_key() or ''
        agent_name = settings.get_agent_name() or ''
        kwargs_ = {
            'debug': True,
            'release': release,
            'environment': settings.get_server_base_url() or '',
            'server_name': f'{agent_name} [{agent_key}]',
            'request_bodies': 'medium',
            'integrations': integrations,
        }
        kwargs_.update(kwargs)

        sentry_sdk.init(packy_agent_sentry_dsn, **kwargs_)
    else:
        logger.warning('Sentry DSN is not configured')
