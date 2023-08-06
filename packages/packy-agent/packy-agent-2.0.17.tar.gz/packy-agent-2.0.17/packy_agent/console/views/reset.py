import logging

import flask
from flask.views import MethodView

from packy_agent.console.forms.action import ActionForm
from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.managers.reset import reset_manager
from packy_agent.domain_logic.managers.network import network_manager
from packy_agent.utils.auth import activation_and_authentication_required, logout
from packy_agent.console.views.base import smart_redirect


OPERATION_DELAY_SECONDS = 5

logger = logging.getLogger(__name__)


def do_action(action):
    if action == 'full_reset':
        if not settings.is_network_configuration_enabled():
            flask.flash(
                'Network configuration is not allowed. Please, see logs for more information')

        logout()
        reset_manager.full_reset(delay_seconds=OPERATION_DELAY_SECONDS)
        flask.flash(f'Reboot will start in {OPERATION_DELAY_SECONDS} seconds...')
    elif action == 'deactivate':
        logout()
        reset_manager.deactivate(delay_seconds=OPERATION_DELAY_SECONDS)
    elif action == 'network_reset':
        if not settings.is_network_configuration_enabled():
            flask.flash(
                'Network configuration is not allowed. Please, see logs for more information')

        reset_manager.reset_network_configuration(reboot_delay_seconds=OPERATION_DELAY_SECONDS)
        flask.flash(f'Reboot will start in {OPERATION_DELAY_SECONDS} seconds...')
    else:
        raise ValueError('Unknown action: {}'.format(action))


class ResetView(MethodView):

    @activation_and_authentication_required
    def get(self):
        form = ActionForm()
        context = {
            'form': form,
            'active_menu_item': 'reset',
            'is_configuration_restorable': network_manager.is_configuration_restorable()
        }

        return flask.render_template('reset.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = ActionForm()
        if form.validate():
            action = flask.request.form['action']
            do_action(action)
            return smart_redirect('success', 'index', button_text='Continue')

        return flask.render_template('reset.html', form=form)
