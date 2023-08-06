import logging

import flask
from flask.views import MethodView

from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.console.forms.action import ActionForm
from packy_agent.console.views.base import smart_redirect
from packy_agent.utils.auth import activation_and_authentication_required
from packy_agent.domain_logic.constants import WORKER_COMPONENT, CONSOLE_COMPONENT


DELAY_SECONDS = 5

logger = logging.getLogger(__name__)


def do_action(action):
    if action == 'reboot':
        flask.flash('Reboot will start in {} seconds...'.format(DELAY_SECONDS))
        control_manager.reboot(delay_seconds=DELAY_SECONDS)
    elif action == 'start_worker':
        control_manager.start(WORKER_COMPONENT)
    elif action == 'stop_worker':
        control_manager.stop(WORKER_COMPONENT)
    elif action == 'restart_worker':
        control_manager.restart(WORKER_COMPONENT)
    elif action == 'restart':
        # Restart is delayed because we need to send HTTP response before Control Server goes down
        flask.flash('Restart will start in {} seconds...'.format(DELAY_SECONDS))
        control_manager.restart_all(delay_seconds=DELAY_SECONDS)
    elif action == 'restart_console':
        # Restart is delayed because we need to send HTTP response before Control Server goes down
        flask.flash('Restart will start in {} seconds...'.format(DELAY_SECONDS))
        control_manager.restart(CONSOLE_COMPONENT, async_delay_seconds=DELAY_SECONDS)
    else:
        raise ValueError('Unknown action: {}'.format(action))


class ControlView(MethodView):

    @activation_and_authentication_required
    def get(self):
        context = {
            'form': ActionForm(),
            'worker_status': control_manager.get_worker_status_line(),
            'active_menu_item': 'control',
        }

        return flask.render_template('control.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = ActionForm()
        if form.validate():
            action = flask.request.form['action']
            do_action(action)
            return smart_redirect('success', 'control')

        return flask.render_template('control.html', form=form)
