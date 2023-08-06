import logging

import flask

import packy_agent
from packy_agent.utils.pkg_resources import get_package_file_full_path
from packy_agent.console.views.index import IndexView
from packy_agent.console.views.login import LoginView, LoginFailureView
from packy_agent.console.views.logout import LogoutView
from packy_agent.console.views.success import SuccessView
from packy_agent.console.views.failure import FailureView
from packy_agent.console.views.network import NetworkView
from packy_agent.console.views.control import ControlView
from packy_agent.console.views.upgrade import UpgradeView
from packy_agent.console.views.reset import ResetView
from packy_agent.console.views.debug import DebugView
from packy_agent.console.views.activate import ActivateView, ActivationFailureView
from packy_agent.console.views import errors as error_handlers
from packy_agent.utils.logging import configure_logging, configure_logging_basic
from packy_agent.utils.installation import (
    dump_version, remove_upgrade_in_progress_lock,
    is_upgrade_in_progress)
from packy_agent.domain_logic.managers.network import network_manager
from packy_agent.utils.platforms import is_inside_docker_container
from packy_agent.clients.sentry import init_sentry_client
from packy_agent.configuration.settings import settings
from packy_agent.utils.misc import generate_flask_secret_key
from packy_agent.domain_logic.constants import CONSOLE_COMPONENT


def configure(app):
    # TODO(dmu) LOW: Refactor to make autooverride from options if there are more options to
    #                override
    mapping = settings.get_console_flask()
    if 'SECRET_KEY' not in mapping:
        settings.set_console_flask_secret_key(generate_flask_secret_key())
        mapping = settings.get_console_flask()

    app.config.from_mapping(mapping)


def setup_routes(app):
    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/network/', view_func=NetworkView.as_view('network'))
    app.add_url_rule('/control/', view_func=ControlView.as_view('control'))
    app.add_url_rule('/upgrade/', view_func=UpgradeView.as_view('upgrade'))
    app.add_url_rule('/reset/', view_func=ResetView.as_view('reset'))
    app.add_url_rule('/debug/', view_func=DebugView.as_view('debug'))
    app.add_url_rule('/success/', view_func=SuccessView.as_view('success'))
    app.add_url_rule('/failure/', view_func=FailureView.as_view('failure'))
    app.add_url_rule('/activate/', view_func=ActivateView.as_view('activate'))
    app.add_url_rule('/activation-failure/',
                     view_func=ActivationFailureView.as_view('activation_failure'))
    app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
    app.add_url_rule('/login-failure/', view_func=LoginFailureView.as_view('login_failure'))
    app.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))


def setup_context_processors(app):

    @app.context_processor
    def extra_context_processor():
        return {
            'version': packy_agent.__version__,
            'is_inside_docker_container': is_inside_docker_container(),
            'is_network_configuration_supported': network_manager.is_network_configuration_supported(),
            'is_upgrade_in_progress': is_upgrade_in_progress,
            'settings': settings,
        }


def setup_error_handlers(app):
    app.register_error_handler(500, error_handlers.handle_http500)
    app.register_error_handler(401, error_handlers.handle_http401)


def get_app(args=None):
    settings.set_runtime('component', CONSOLE_COMPONENT)

    if args:
        log_level = args.log_level
        cargs_console = vars(args)
        del cargs_console['log_level']
        cargs = {
            'log_level': log_level,
            'console': cargs_console,
        }
        settings.set_commandline_arguments(cargs)
    else:
        log_level = logging.WARNING

    configure_logging_basic(log_level)

    settings.validate()

    init_sentry_client()
    configure_logging(log_level)

    app = flask.Flask(__name__,
                      template_folder=get_package_file_full_path(__name__, 'templates'),
                      static_folder=get_package_file_full_path(__name__, 'static'),
                      static_url_path='/assets')
    configure(app)
    setup_routes(app)
    setup_context_processors(app)
    setup_error_handlers(app)

    remove_upgrade_in_progress_lock()
    dump_version(settings.get_console_version_dump_filename(),
                 settings.get_console_version_dump_variable_name())
    settings.update_started_at_ts()

    return app
