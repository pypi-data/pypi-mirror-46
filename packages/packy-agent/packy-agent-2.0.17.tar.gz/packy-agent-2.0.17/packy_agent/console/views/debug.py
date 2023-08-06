import logging
from tailer import Tailer

import flask
from flask.views import MethodView

from packy_agent.configuration.settings import settings
from packy_agent.utils.auth import activation_and_authentication_required

TAIL_SIZE = 100


logger = logging.getLogger(__name__)


def tail(filename, size=TAIL_SIZE):
    try:
        with open(filename, encoding='utf-8', errors='ignore') as f:
            return '\n'.join(Tailer(f).tail(size))
    except Exception as ex:
        return f'Exception occurred while reading log file: {ex!r}'


class DebugView(MethodView):

    @activation_and_authentication_required
    def get(self):

        logs = (
            ('Supervisor log', settings.get_supervisor_log_filename(),
             tail(settings.get_supervisor_log_filename())),
            ('Worker stdout log', settings.get_worker_stdout_log_filename(),
             tail(settings.get_worker_stdout_log_filename())),
            ('Worker stderr log', settings.get_worker_stderr_log_filename(),
             tail(settings.get_worker_stderr_log_filename())),
            ('Console stdout log', settings.get_console_stdout_log_filename(),
             tail(settings.get_console_stdout_log_filename())),
            ('Console stderr log', settings.get_console_stderr_log_filename(),
             tail(settings.get_console_stderr_log_filename())),
        )

        context = {
            'enumerated_settings': enumerate(settings.labeled_items(), start=1),
            'logs': logs,
            'active_menu_item': 'debug',
        }

        return flask.render_template('debug.html', **context)
