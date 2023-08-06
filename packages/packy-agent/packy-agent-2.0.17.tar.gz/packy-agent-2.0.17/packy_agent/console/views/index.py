import logging

import flask
from flask.views import MethodView

from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.utils.auth import activation_and_authentication_required

logger = logging.getLogger(__name__)


class IndexView(MethodView):

    @activation_and_authentication_required
    def get(self):
        context = {
            'worker_status': control_manager.get_worker_status_line(),
            'active_menu_item': 'status',
        }
        return flask.render_template('index.html', **context)

