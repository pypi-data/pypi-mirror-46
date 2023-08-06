import logging
import base64
import socket
from functools import wraps
from urllib.parse import urljoin, urlencode

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

import packy_agent
from packy_agent.exceptions import ImproperlyConfiguredError, NoAccessTokenError
from packy_agent.configuration.settings import settings
from packy_agent.utils.misc import get_lazy_value
from packy_agent.utils.platforms import get_platform
from packy_agent.exceptions import AuthenticationError
from packy_agent.utils.collections import set_if
from packy_agent.utils.container import container
from packy_agent.utils.data_usage import get_network_usage


logger = logging.getLogger(__name__)

OAUTH_TOKEN_PATH = 'oauth/token/'

API_V2_BASE_URL = 'api/v2/'

PENDING_AGENT_PATH = API_V2_BASE_URL + 'pending-agent/'
AGENT_VERSION_PATH = API_V2_BASE_URL + 'agent-version/'
USER_AGENT_TEMPLATE_PATH = API_V2_BASE_URL + 'user/agent/'
AGENT_TEMPLATE_PATH = API_V2_BASE_URL + 'agent/'
MEASUREMENT_TEMPLATE_PATH = AGENT_TEMPLATE_PATH + 'module/{}/measurement/'
AGENT_INSTANCE_TEMPLATE_PATH = USER_AGENT_TEMPLATE_PATH + '{}/'


METHOD_MAP = {
    'GET': requests.get,
    'POST': requests.post,
    'PATCH': requests.patch,
}

GET_INACTIVE_AGENTS_PARAMS = urlencode({'fields': 'id,name', 'is_active': 'false'})


def make_basic_authorization_value(username, password):
    return 'Basic ' + base64.b64encode((username + ':' + password).encode()).decode()


def make_token_authorization_value(access_token):
    return 'Bearer ' + access_token


def generate_agent_name():
    return socket.gethostname()


def if_callable(value):
    return value is not None


def with_agent_access_token(func_or_meth):
    @wraps(func_or_meth)
    def wrapper(*args, **kwargs):
        if not settings.get_access_token():
            raise NoAccessTokenError()
        return func_or_meth(*args, **kwargs)

    return wrapper


class PackyServerClient:
    # TODO(dmu) HIGH: Implement support for persistent HTTP?

    def __init__(self, base_url=None, timeout=None):
        self._base_url = base_url or settings.get_server_base_url
        self._timeout = timeout or settings.get_http_timeout_seconds

        self._user_agent = 'packy-agent/{} ({})'.format(packy_agent.__version__, get_platform())

    @property
    def base_url(self):
        base_url = get_lazy_value(self._base_url)
        if not base_url:
            raise ImproperlyConfiguredError('Packy Server base URL is not configured')
        return base_url

    @property
    def timeout(self):
        return get_lazy_value(self._timeout)

    def make_url(self, path):
        return urljoin(self.base_url, path)

    # TODO(dmu) MEDIUM: Get rid of `auto_login`. Support multiple authentication methods instead
    def request(self, url, data=None, json=None, method=None, headers=None,
                authorization=None, raise_for_status=True):

        if not method:
            if data is not None or json is not None:
                method = 'POST'
            else:
                method = 'GET'

        python_method = METHOD_MAP.get(method)
        if not python_method:
            raise NotImplementedError('Method {} is not supported'.format(method))

        if not authorization:
            access_token = settings.get_access_token()
            if access_token:
                authorization = make_token_authorization_value(access_token)

        # TODO(dmu) HIGH: Implement token expiration support
        # if auto_login and (not self.token or time.time() >= self.token_expiration):
        #     self.login()

        headers = headers.copy() if headers else {}
        if authorization:
            headers.setdefault('Authorization', authorization)
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('User-Agent', self._user_agent)

        logger.debug(f'HTTP {method} {url} "{data or json}" request')
        response = python_method(url, data=data, json=json, headers=headers, timeout=self.timeout)

        if response.status_code >= 400:
            logger.debug('HTTP%s: %s', response.status_code, response.content)

        if raise_for_status:
            response.raise_for_status()

        return response

    # E-mail/password authentication methods
    ########################################

    def get_inactive_agents(self, email, password, raise_for_status=True):
        return self.request(
            self.make_url(USER_AGENT_TEMPLATE_PATH) + '?' + GET_INACTIVE_AGENTS_PARAMS,
            authorization=make_basic_authorization_value(email, password),
            raise_for_status=raise_for_status)

    def create_agent(self, email, password, raise_for_status=True):
        payload = {'name': generate_agent_name()}
        return self.request(self.make_url(USER_AGENT_TEMPLATE_PATH), json=payload,
                            authorization=make_basic_authorization_value(email, password),
                            raise_for_status=raise_for_status)

    def activate_agent(self, agent_id, authorization, raise_for_status=True):
        url = (self.make_url(AGENT_INSTANCE_TEMPLATE_PATH).format(agent_id) + '?' +
               urlencode({'with_configuration': 'yes'}))
        return self.request(url, json={'is_active': True}, method='PATCH',
                            authorization=authorization, raise_for_status=raise_for_status)

    def activate_agent_basic_auth(self, email, password, agent_id, raise_for_status=True):
        return self.activate_agent(agent_id=agent_id,
                                   authorization=make_basic_authorization_value(email, password),
                                   raise_for_status=raise_for_status)

    def validate_auth(self, email, password, agent_key=None):
        agent_key = agent_key or settings.get_agent_key()
        if not agent_key:
            raise ImproperlyConfiguredError('`agent_key` must be provided')

        # Use filter to get the agent by key
        url = self.make_url(
            USER_AGENT_TEMPLATE_PATH) + '?' + urlencode(
                {'fields': 'key,user', 'expand': 'user', 'key': agent_key})
        response = self.request(url, authorization=make_basic_authorization_value(email, password),
                                raise_for_status=False)
        status_code = response.status_code

        # Credentials may be invalid themselves (i.e. typo in password)
        if status_code == 401:
            logger.info('Invalid credentials')
            return False

        # There may be other errors
        response.raise_for_status()

        # Server should respond with a list, but in case it does not we take care
        # (this should never happen).
        response_json = response.json()
        if not isinstance(response_json, list):
            logger.warning('Server responded with %r instead of a list', response_json)
            return False

        # List is empty. This may mean that agent was deleted on server or that credentials
        # provided belong to another user (not the one agent belongs to)
        if not response_json:
            return False

        # List is longer than 1 item. Something went wrong on server (this should never happen).
        if len(response_json) > 1:
            logger.warning('Server returned multiple agents instead of one')
            return False

        agent_json = response_json[0]
        # Double check that we got email we expected
        if (agent_json.get('user') or {}).get('email') != email:
            logger.warning('Server returned agent of another user')
            return False

        # Double check that we got key we expected
        if agent_json['key'] != agent_key:
            logger.warning('Server returned another agent')
            return False

        return True

    # Client secret authentication methods
    ######################################
    def get_access_token_for_credentials(self, client_id, client_secret):
        # TODO(dmu) HIGH: Remove this method once all agents migrate to v2
        url = self.make_url(OAUTH_TOKEN_PATH)
        response = self.request(url, data={'grant_type': 'client_credentials',
                                           'client_id': client_id,
                                           'client_secret': client_secret},
                                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                raise_for_status=False)
        if response.status_code == 200:
            response_json = response.json()
            return response_json['access_token']
        else:
            raise AuthenticationError('Not authenticated: %s', response.content)

    # Refresh token authentication methods
    ######################################
    def refresh_access_token(self, client_id, refresh_token):
        url = self.make_url(OAUTH_TOKEN_PATH)
        response = self.request(url, data={'grant_type': 'refresh_token',
                                           'client_id': client_id,
                                           'refresh_token': refresh_token},
                                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                raise_for_status=False)
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        elif status_code == 401:
            raise AuthenticationError('Not authenticated: %s', response.content)
        else:
            response.raise_for_status()

    # No authentication methods
    ###########################
    def notify_server(self, agent_console_url):
        url = self.make_url(PENDING_AGENT_PATH)
        payload = {
            'agent_control_server_url': agent_console_url,  # TODO(dmu) LOW: Legacy, remove
            'agent_console_url': agent_console_url,
        }
        try:
            requests.post(url, json=payload, timeout=self.timeout)
        except RequestsConnectionError:
            logger.info('Unable to notify: Packy Server unavailable')

    def get_version_max(self):
        url = self.make_url(AGENT_VERSION_PATH)
        response = self.request(url)
        return response.json().get('version_max')

    # Access token authentication methods
    #####################################
    def activate_agent_token_auth(self, access_token, agent_id, raise_for_status=True):
        return self.activate_agent(agent_id=agent_id,
                                   authorization=make_token_authorization_value(access_token),
                                   raise_for_status=raise_for_status)

    def deactivate_agent_legacy(self, access_token, agent_id):
        return self.request(self.make_url(AGENT_INSTANCE_TEMPLATE_PATH.format(agent_id)),
                            json={'is_active': False}, method='PATCH',
                            authorization=make_token_authorization_value(access_token))

    @with_agent_access_token
    def deactivate_agent(self):
        return self.request(self.make_url(AGENT_TEMPLATE_PATH),
                            json={'is_active': False}, method='PATCH')

    @with_agent_access_token
    def submit_measurement(self, module_public_identifier, measurement, raise_for_status=True):
        url = self.make_url(MEASUREMENT_TEMPLATE_PATH.format(module_public_identifier))
        return self.request(url, data=measurement, raise_for_status=raise_for_status)

    @with_agent_access_token
    def update_status(self, version, ip_address=None, is_online=True):
        payload = {
            'is_online': is_online,
            'version': version,
        }

        set_if(payload, 'ip_address', ip_address)

        bytes_sent, bytes_received = get_network_usage()
        set_if(payload, 'bytes_sent', bytes_sent, if_callable=if_callable)
        set_if(payload, 'prev_bytes_sent', settings.get('bytes_sent'), if_callable=if_callable)
        set_if(payload, 'bytes_received', bytes_received, if_callable=if_callable)
        set_if(payload, 'prev_bytes_received', settings.get('bytes_received'),
               if_callable=if_callable)

        url = self.make_url(AGENT_TEMPLATE_PATH)
        try:
            response = self.request(url, json=payload, method='PATCH', raise_for_status=False)
        except RequestsConnectionError:
            logger.info('Unable to update status (send heartbeat): Packy Server unavailable')
            return
        else:
            status_code = response.status_code
            if status_code == 200:
                settings.set('bytes_sent', bytes_sent)
                settings.set('bytes_received', bytes_received)
            elif status_code == 401:
                logger.debug('Access token is invalid')
                # We do not expect context switch here because we work with RAM only (no IO)
                invalid_access_tokens = settings.get_invalid_access_tokens() or set()
                invalid_access_tokens.add(settings.get_access_token())
                settings.set_runtime('invalid_access_tokens', invalid_access_tokens)
            elif status_code >= 500:
                logger.info('Packy Server responded with HTTP%s', status_code)
            elif status_code >= 400:
                response.raise_for_status()
            else:
                logger.warning('Unexpected status while sending heartbeat: HTTP%s', status_code)

        return response

    @with_agent_access_token
    def get_settings(self):
        url = self.make_url(AGENT_TEMPLATE_PATH) + '?fields=settings'
        response = self.request(url)
        return response.json()['settings']

    @with_agent_access_token
    def is_agent_online(self):
        url = self.make_url(AGENT_TEMPLATE_PATH) + '?fields=is_online'
        response = self.request(url)
        response.raise_for_status()
        return response.json().get('is_online')


def get_inactive_agents(email, password):
    response = get_packy_server_client().get_inactive_agents(email, password, raise_for_status=False)

    if response.status_code == 401:
        raise AuthenticationError('Invalid credentials for agent activation')

    response.raise_for_status()
    return {agent['id']: agent['name'] for agent in response.json()}


def get_packy_server_client():
    client = getattr(container, 'packy_server_client', None)
    if not client:
        container.packy_server_client = client = PackyServerClient()

    return client
