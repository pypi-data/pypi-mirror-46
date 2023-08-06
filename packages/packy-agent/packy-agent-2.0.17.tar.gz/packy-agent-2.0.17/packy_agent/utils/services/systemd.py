import os
import stat
from io import StringIO

from packy_agent.utils.services.base import ServiceBase
from packy_agent.utils.shell import run_command
from packy_agent.utils.output import write_to_console_or_file


class SystemdService(ServiceBase):

    RELOAD_SYSTEMD_CONFIGURATION_COMMAND = 'systemctl daemon-reload'
    MAKE_START_ON_REBOOT_COMMAND_TEMPLATE = 'update-rc.d {name} defaults'

    SERVICE_COMMAND_TEMPLATE = 'service {name} {command}'
    SYSTEMCTL_COMMAND_TEMPLATE = 'systemctl {command} {name}.service'

    INITD_PATH_TEMPLATE = '/etc/init.d/{name}'
    # TODO(dmu) MEDIUM: Is `UNIT_SERVICE_PATH_TEMPLATE` different on OSes other than Ubuntu
    UNIT_SERVICE_PATH_TEMPLATE = '/lib/systemd/system/{name}.service'

    def __init__(self, name):
        super(SystemdService, self).__init__(name)

        self.make_start_on_reboot_command = self.MAKE_START_ON_REBOOT_COMMAND_TEMPLATE.format(
            name=name)

        self.initd_path = self.INITD_PATH_TEMPLATE.format(name=name)
        self.unit_service_path = self.UNIT_SERVICE_PATH_TEMPLATE.format(name=name)

    @classmethod
    def get_template(cls, is_systemctl=False):
        return cls.SYSTEMCTL_COMMAND_TEMPLATE if is_systemctl else cls.SERVICE_COMMAND_TEMPLATE

    @classmethod
    def reload_systemd_configuration(cls, raise_exception=False):
        run_command(cls.RELOAD_SYSTEMD_CONFIGURATION_COMMAND, raise_exception=raise_exception)

    def run_basic_command(self, command, is_systemctl=False, raise_exception=False,
                          is_async=False):
        command = self.get_template(
            is_systemctl=is_systemctl).format(name=self.name, command=command)
        return run_command(command, raise_exception=raise_exception, is_async=is_async)

    def start(self, is_systemctl=False, raise_exception=False):
        self.run_basic_command('start', is_systemctl=is_systemctl, raise_exception=raise_exception)

    def stop(self, is_systemctl=False, raise_exception=False, is_async=False):
        self.run_basic_command('stop', is_systemctl=is_systemctl, raise_exception=raise_exception,
                               is_async=is_async)

    def restart(self, is_systemctl=False, raise_exception=False):
        self.run_basic_command('restart', is_systemctl=is_systemctl,
                               raise_exception=raise_exception)

    def reload(self, is_systemctl=False, raise_exception=False):
        self.run_basic_command('reload', is_systemctl=is_systemctl,
                               raise_exception=raise_exception)

    def make_start_on_reboot(self, raise_exception=False):
        run_command(self.make_start_on_reboot_command, raise_exception=raise_exception)

    def enable_unit_service(self, raise_exception=False):
        self.run_basic_command('enable', is_systemctl=True, raise_exception=raise_exception)

    def update_initd_script(self, content):
        initd_path = self.initd_path
        write_to_console_or_file(initd_path, content)
        os.chmod(initd_path, os.stat(initd_path).st_mode | stat.S_IEXEC)
        self.reload_systemd_configuration(raise_exception=True)
        self.make_start_on_reboot(raise_exception=True)

    def update_unit_service_configuration(self, content):
        write_to_console_or_file(self.unit_service_path, content)
        self.enable_unit_service(raise_exception=True)
        self.reload_systemd_configuration(raise_exception=True)
        self.restart(is_systemctl=True, raise_exception=True)

    def is_active(self, raise_exception=False):
        output = self.run_basic_command('is-active',
                                        is_systemctl=True, raise_exception=raise_exception)
        return output == 'active'

    def is_running(self):
        return self.is_active()

    def get_property(self, name, raise_exception=False):
        prefix = name + '='
        output = self.run_basic_command('show', is_systemctl=True, raise_exception=raise_exception)
        if output:
            for line in StringIO(output.decode('utf-8')):
                line = line.rstrip('\n\r')
                if line.startswith(prefix):
                    return line[len(prefix):]

    def get_pid(self, raise_exception=False):
        value = self.get_property('MainPID', raise_exception=raise_exception)
        try:
            return int(value)
        except (TypeError, ValueError):
            return None


packy_service = SystemdService('packy')
nginx_service = SystemdService('nginx')
log2ram_service = SystemdService('log2ram')
