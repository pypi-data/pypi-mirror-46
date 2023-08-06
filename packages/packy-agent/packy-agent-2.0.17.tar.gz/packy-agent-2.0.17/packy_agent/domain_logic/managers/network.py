import re
import shutil
import os.path
import logging
from io import StringIO

from jinja2 import Template
import netifaces

from packy_agent.utils.misc import atomic_write
from packy_agent.utils.pkg_resources import get_package_file_content
from packy_agent.utils.shell import run_command_async
from packy_agent.utils.platforms import (get_os_id_and_version, LINUX_MINT_18_1, UBUNTU_16_04,
                                         UBUNTU_18_04, RASPBIAN_9, is_inside_docker_container)
from packy_agent.configuration.settings import settings
from packy_agent.utils.network import get_interfaces
from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.utils.network import get_actual_ip_address


STATIC_TEMPLATE_TYPE = 'static'
DHCP_TEMPLATE_TYPE = 'dhcp'

UBUNTU_DEBIAN_TEMPLATES = {
    STATIC_TEMPLATE_TYPE: 'configuration/templates/network/ubuntu-debian/static',
    DHCP_TEMPLATE_TYPE: 'configuration/templates/network/ubuntu-debian/dhcp'
}

OPERATING_SYSTEM_TEMPLATES = {
    LINUX_MINT_18_1: UBUNTU_DEBIAN_TEMPLATES,
    UBUNTU_16_04: UBUNTU_DEBIAN_TEMPLATES,
    UBUNTU_18_04: UBUNTU_DEBIAN_TEMPLATES,
    RASPBIAN_9: UBUNTU_DEBIAN_TEMPLATES,
}

STANZA_RE = re.compile(r'^\s*(?:iface|mapping|auto|allow-\S+|source|source-directory)')
IFACE_STANZA_RE = re.compile(r'^\s*iface\s+(?P<iface>[^\s:]+)(?::\S+)?\s+inet\s+(?P<method>\S+)')
AUTO_STANZA_RE = re.compile(r'^\s*(auto|allow-auto)\s+(?P<iface>\S+)')


BACKUP_FILENAME_TEMPLATE = '{}.packy.backup'

ATTRS_RE = {
    'ip_address': re.compile('\s*address\s+(\S+)'),
    'subnet_mask': re.compile('\s*netmask\s+(\S+)'),
    'default_gateway': re.compile('\s*gateway\s+(\S+)'),
    'name_servers': re.compile('\s*dns-nameservers\s+(.*)'),
}
ANY_SPACE_RE = re.compile('\s+')

logger = logging.getLogger(__name__)


def update_network(interface, delay_seconds=0):
    run_command_async(f'ip addr flush {interface}; systemctl restart networking.service',
                      delay_seconds=delay_seconds)


def get_backup_filename(original_filename):
    return BACKUP_FILENAME_TEMPLATE.format(original_filename)


def get_stanzas():
    configuration_filename = settings.get_interfaces_configuration_filename()

    stanzas = []

    lines = []
    stanzas.append(lines)
    with open(configuration_filename) as f:
        for line in f:
            match = STANZA_RE.match(line)
            if match:
                lines = []
                stanzas.append(lines)

            lines.append(line)

    return stanzas


def get_stanza_by_interface(interface, stanzas=None):
    stanzas = get_stanzas() if stanzas is None else stanzas
    for lines in stanzas:
        if lines:
            first_line = lines[0]
            match = IFACE_STANZA_RE.match(first_line)
            if match and match.group('iface') == interface:
                return lines


def get_stanza_attributes(stanza):
    attrs = {}
    for line in stanza:
        for attr_name, regex in ATTRS_RE.items():
            match = regex.match(line)
            if match:
                attrs[attr_name] = match.group(1)

    return attrs


def get_replacing_content(interface, is_dhcp, context=None):
    os_id_and_version = get_os_id_and_version()
    template_paths = OPERATING_SYSTEM_TEMPLATES.get(os_id_and_version)
    if not template_paths:
        raise NotImplementedError(f'Operating system with with this ID is not supported: '
                                  f'{os_id_and_version[0]}')

    template_path = template_paths[DHCP_TEMPLATE_TYPE if is_dhcp else STATIC_TEMPLATE_TYPE]
    template = Template(get_package_file_content('packy_agent', template_path).decode('utf-8'))

    context = context or {}
    context['interface'] = interface
    return '\n\n' + template.render(**context) + '\n\n'


def get_interfaces_configuration_file_stream(interface, replacing_content):
    stream = StringIO()

    for lines in get_stanzas():
        if lines:
            first_line = lines[0]
            match = AUTO_STANZA_RE.match(first_line)
            if match and match.group('iface') == interface:
                continue

            match = IFACE_STANZA_RE.match(first_line)
            if match and match.group('iface') == interface:
                stream.write(replacing_content)
                replacing_content = ''
                continue

        for line in lines:
            stream.writelines(line)

    stream.write(replacing_content)
    stream.seek(0)

    return stream


class NetworkManager:

    @staticmethod
    def backup_configuration():
        original_filename = settings.get_interfaces_configuration_filename()
        backup_filename = get_backup_filename(original_filename)

        if not os.path.isfile(backup_filename):
            try:
                shutil.copy(original_filename, backup_filename)
            except FileNotFoundError:
                pass

    @staticmethod
    def is_configuration_restorable():
        return os.path.isfile(get_backup_filename(settings.get_interfaces_configuration_filename()))

    @staticmethod
    def restore_configuration(reboot=True, reboot_delay_seconds=5):
        if settings.is_network_configuration_enabled():
            original_filename = settings.get_interfaces_configuration_filename()
            backup_filename = get_backup_filename(settings.get_interfaces_configuration_filename())
            if os.path.isfile(backup_filename):
                try:
                    os.replace(backup_filename, original_filename)
                except Exception as ex:
                    logger.warning('Could not restore network configuration: %s', ex)
                else:
                    if reboot:
                        control_manager.reboot(delay_seconds=reboot_delay_seconds)
            else:
                logger.debug('Backup file %s was not found', backup_filename)
        else:
            logger.info('Network configuration change is disabled (for developer protection)')

    def get_configuration(self, interface):
        # TODO(dmu) MEDIUM: Implement more precise DHCP detection
        interface_stanza = get_stanza_by_interface(interface)
        if interface_stanza:
            match = IFACE_STANZA_RE.match(interface_stanza[0])
            is_dhcp = match and match.group('method') == 'dhcp'

            attributes = get_stanza_attributes(interface_stanza)
            attributes['dhcp'] = is_dhcp

            name_servers = attributes.get('name_servers')
            if name_servers is not None:
                attributes['name_servers'] = ','.join(ANY_SPACE_RE.split(name_servers.strip()))

            return attributes
        else:
            # We consider DHCP if interface is not configured in /etc/network/interfaces
            return {'dhcp': True}

    def is_network_configuration_supported(self):
        return (settings.is_vendored_hardware() and
                not is_inside_docker_container() and
                get_os_id_and_version() in OPERATING_SYSTEM_TEMPLATES)

    def get_configurable_network_interface(self):
        explicit_interface = settings.get_configurable_network_interface()
        if explicit_interface:
            return explicit_interface

        interfaces = get_interfaces()
        interfaces.remove('lo')  # do not consider local interface
        candidates = list(filter(lambda x: ':' not in x, interfaces))  # filter virtual interfaces
        if len(candidates) > 1:
            actual_ip_address = get_actual_ip_address()
            for interface in candidates.copy():
                ifaddresses = netifaces.ifaddresses(interface)
                for ipv4_address in ifaddresses.get(netifaces.AF_INET) or ():
                    if ipv4_address.get('addr') == actual_ip_address:
                        break
                else:
                    candidates.remove(interface)

        if candidates:
            if len(candidates) == 1:
                return candidates[0]
            else:
                logger.warning('Could not detect configurable network interface')
        else:
            logger.debug('No configurable network interface found')

    def set_network(self, interface, is_dhcp, context=None, reboot_delay_seconds=5,
                    no_backup=False):
        if not self.is_network_configuration_supported():
            raise NotImplementedError('Network configuration is not supported for this platform')

        replacing_content = get_replacing_content(interface, is_dhcp, context=context)
        stream = get_interfaces_configuration_file_stream(interface, replacing_content)

        if settings.is_network_configuration_enabled():
            if not no_backup:
                self.backup_configuration()

            with atomic_write(settings.get_interfaces_configuration_filename(),
                              overwrite=True) as f:
                f.write(stream.read())

            if reboot_delay_seconds is not None:
                control_manager.reboot(delay_seconds=reboot_delay_seconds,
                                       change_worker_stopped_status=False)
            # TODO(dmu) MEDIUM: Improve to change IP address without reboot (this includes proper
            #                   of restart Worker, Console and Watchdog to use updated network
            #                   settings)
            # update_network(interface, delay_seconds=self.update_network_delay_seconds)
        else:
            logger.info('Network configuration change was disabled (for developer protection)')
            logger.debug('Generated interfaces configuration file content:\n%s', stream.read())

    def set_static_ip_address(self, interface, ip_address, subnet_mask, default_gateway,
                              name_servers=('8.8.8.8', '8.8.4.4'), reboot_delay_seconds=5):
        context = {
            'ip_address': ip_address,
            'subnet_mask': subnet_mask,
            'default_gateway': default_gateway,
            'name_servers': name_servers,
        }
        self.set_network(interface, is_dhcp=False, context=context,
                         reboot_delay_seconds=reboot_delay_seconds)

    def set_dhcp(self, interface=None, reboot_delay_seconds=5, no_backup=False):
        interface = interface or self.get_configurable_network_interface()
        self.set_network(interface, is_dhcp=True, reboot_delay_seconds=reboot_delay_seconds,
                         no_backup=no_backup)


# As long as manager is stateless object we do not need to care about greenlet-multitasking safety
network_manager = NetworkManager()
