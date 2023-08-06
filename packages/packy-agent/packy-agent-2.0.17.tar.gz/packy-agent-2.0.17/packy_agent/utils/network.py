from urllib.parse import urlparse

import socket
import warnings

import netifaces

from packy_agent.configuration.settings import settings

DEFAULT_HOST_TO_REACH = '10.255.255.255'


def get_machine_ip_address(host_to_reach=DEFAULT_HOST_TO_REACH):
    # As suggested here:
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

    # TODO(dmu) HIGH: Support multiple interfaces properly (how is it?)
    socket_obj = None
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # to report the interface that is actually used for connection to Packy Server
            socket_obj.connect((host_to_reach, 1))
        except Exception:
            # destination does not have to be reachable
            socket_obj.connect((DEFAULT_HOST_TO_REACH, 1))
        return socket_obj.getsockname()[0]
    except Exception:
        warnings.warn('Could not get actual IP address')
        return
    finally:
        if socket_obj:
            socket_obj.close()


def get_hostname_from_url(url):
    return urlparse(url).netloc.split(':')[0]


def get_interfaces():
    return netifaces.interfaces()


def get_actual_ip_address():
    return get_machine_ip_address(get_hostname_from_url(settings.get_server_base_url()))
