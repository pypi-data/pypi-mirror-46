import logging
import os
import os.path
from urllib.parse import urlencode

from filelock import FileLock, Timeout
from jinja2 import Template
from pkg_resources import parse_version

from packy_agent.configuration.settings import settings
from packy_agent.exceptions import AuthenticationError, ValidationError
from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.domain_logic.constants import WORKER_COMPONENT
from packy_agent.utils.pkg_resources import get_package_file_content
from packy_agent.utils.shell import run_command_async
from packy_agent.utils.output import write_to_console_or_file
from packy_agent.clients.packy_server import get_packy_server_client


PACKY_GET_INSTALL_SCRIPT_PATH = '/tmp/packy-run-install-script.sh'


logger = logging.getLogger(__name__)


def render_template_from_package_file_content(template_module_name, template_filename,
                                              context=None):
    template = Template(
        get_package_file_content(template_module_name, template_filename).decode('utf-8'))
    return template.render(**(context or {}))


def validate_version(version):
    version_max = get_packy_server_client().get_version_max()
    if version_max is None:
        return version

    if version is None:
        return version_max

    if parse_version(version) > parse_version(version_max):
        raise ValueError(f'Could not install/upgrade to version {version} '
                         f'(it is higher than {version_max})')

    return version


def generate_packy_run_install_script(script_filename, version):
    context = {'with_shebang': True}
    if version:
        context['download_args'] = '?{}'.format(urlencode({'version': version}))

    write_to_console_or_file(
        script_filename,
        render_template_from_package_file_content(
            'packy_agent', 'scripts/misc/packy-run-install-script.sh.j2', context))


def run_packy_run_install_script(script_filename, upgrade_in_progress_lock_filename, delay_seconds):
    extra_envvars = {
        'PACKY_SERVER_BASE_URL': settings.get_server_base_url(),
        'PACKY_AGENT_ACCESS_TOKEN': settings.get_access_token(),
    }

    old_path = os.getenv('OLD_PATH')
    if old_path:
        extra_envvars['PATH'] = old_path

    export_envvars = ' '.join(f"export {k}='{v}';" for k, v in extra_envvars.items())
    command = (f'{export_envvars} /bin/bash {script_filename}; '
               f'rm -f {upgrade_in_progress_lock_filename}')

    run_command_async(command, delay_seconds=delay_seconds)


def refresh_access_token():
    old_access_token = settings.get_access_token()

    tokens = get_packy_server_client().refresh_access_token(
        settings.get_client_id(), settings.get_refresh_token())
    settings.set_access_token(tokens['access_token'])
    settings.set_refresh_token(tokens['refresh_token'])

    invalid_access_tokens = settings.get_invalid_access_tokens()
    if invalid_access_tokens:
        invalid_access_tokens.discard(old_access_token)


class InstallAndUpgradeManager:

    def activate(self, email=None, password=None, access_token=None, agent_id=None,
                 ensure_restarted=True):
        if (email is None or password is None) and access_token is None:
            raise ValueError('Either email and password or access_token must be provided')

        if settings.is_activated():
            raise ValidationError('Agent has already been activated')

        if agent_id is None:
            response = get_packy_server_client().create_agent(email, password, raise_for_status=False)
        elif access_token is None:
            response = get_packy_server_client().activate_agent_basic_auth(
                email, password, agent_id, raise_for_status=False)
        else:
            response = get_packy_server_client().activate_agent_token_auth(
                access_token, agent_id, raise_for_status=False)

        status_code = response.status_code
        if status_code == 401:
            raise AuthenticationError('Invalid credentials for agent activation')
        elif status_code == 400:
            payload = response.json()
            errors = payload.get('errors') or {}
            non_field_errors = errors.pop('non_field_errors', None) or []
            messages = ([payload.get('message')] +
                        [nfe.get('message') for nfe in non_field_errors] +
                        ['{}: {}.'.format(k, v.get('message')) for k, v in errors.items()])

            raise ValidationError(' '.join(filter(None, messages)))

        response.raise_for_status()

        response_json = response.json()
        settings.activate(
            client_id=response_json['client_id'],
            access_token=response_json['access_token'],
            refresh_token=response_json['refresh_token'],
            agent_key=response_json['key'],
            agent_name=response_json['name'],
        )

        if ensure_restarted:
            if control_manager.is_running(WORKER_COMPONENT):
                control_manager.restart(WORKER_COMPONENT)
            else:
                control_manager.start(WORKER_COMPONENT)

    def install_and_restart(self, version=None, delay_seconds=None):
        logger.info('Upgrading...')
        if not settings.is_upgrade_enabled():
            logger.info('Upgrade was disabled (for developer protection)')
            return

        upgrade_in_progress_lock_filename = settings.get_upgrade_in_progress_lock_filename()
        file_lock = FileLock(upgrade_in_progress_lock_filename)
        try:
            with file_lock.acquire(timeout=1):
                version = validate_version(version)

                script_filename = settings.get_packy_run_install_script_filename()
                generate_packy_run_install_script(script_filename, version)
                run_packy_run_install_script(script_filename, upgrade_in_progress_lock_filename,
                                             delay_seconds)
        except Timeout:
            logger.info('Concurrent upgrade detected')

    def upgrade_and_restart(self, delay_seconds=None):
        self.install_and_restart(delay_seconds=delay_seconds)


# As long as manager is stateless object we do not need to care about greenlet-multitasking safety
install_and_upgrade_manager = InstallAndUpgradeManager()
