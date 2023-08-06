import logging

from packy_agent.configuration.settings import settings
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.domain_logic.managers.install_and_upgrade import refresh_access_token
from packy_agent.constants import GUARD_LOOP

logger = logging.getLogger(__name__)


def guard():
    if settings.get_access_token() in (settings.get_invalid_access_tokens() or ()):
        refresh_access_token()

    if settings.has_settings_changed_on_server():
        logger.warning('Apparently we missed reload event, will handle it now')
        # Although we apply new settings on fly we still need to restart everything in case
        # settings that are only once on start are changed
        control_manager.restart_all()


class GuardLoop(PeriodicLoop):

    formal_name = GUARD_LOOP

    def __init__(self, period):
        super().__init__(period=period, callable_=guard)
