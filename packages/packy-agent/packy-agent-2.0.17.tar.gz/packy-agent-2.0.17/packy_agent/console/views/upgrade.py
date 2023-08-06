import logging

import flask
from flask.views import MethodView

from packy_agent.domain_logic.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.console.forms.action import ActionForm
from packy_agent.configuration.settings import settings
from packy_agent.console.views.base import smart_redirect
from packy_agent.utils.auth import activation_and_authentication_required
from packy_agent.utils.installation import is_upgrade_in_progress


DELAY_SECONDS = 5

logger = logging.getLogger(__name__)


class UpgradeView(MethodView):

    @activation_and_authentication_required
    def get(self):
        form = ActionForm()
        context = {
            'form': form,
            'active_menu_item': 'upgrade',
        }

        return flask.render_template('upgrade.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = ActionForm()
        if form.validate():
            action = flask.request.form['action']
            if action == 'upgrade_and_restart':
                if is_upgrade_in_progress():
                    flask.flash('Concurrent upgrade detected')
                    return smart_redirect('failure', 'upgrade')
                else:
                    flask.flash(
                        'Upgrade and restart will start in {} seconds...'.format(DELAY_SECONDS))
                    install_and_upgrade_manager.upgrade_and_restart(DELAY_SECONDS)
            else:
                raise ValueError('Unknown action: {}'.format(action))

            if not settings.is_upgrade_enabled():
                flask.flash('Please, see logs for more information')

            return smart_redirect('success', 'upgrade')

        return flask.render_template('upgrade.html', form=form)
