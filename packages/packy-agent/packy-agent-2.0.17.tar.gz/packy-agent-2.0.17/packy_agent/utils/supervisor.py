import logging
from io import BytesIO

import supervisor.supervisorctl
from supervisor.options import ClientOptions

from packy_agent.configuration.settings import settings
from packy_agent.utils.misc import get_executable_path
from packy_agent.utils.shell import run_command_async

logger = logging.getLogger(__name__)


class CustomController(supervisor.supervisorctl.Controller):

    def output(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        self.stdout.write(message + b'\n')


def supervisor_main(args=None, options=None, stdout=None):
    if options is None:
        options = ClientOptions()

    options.realize(args, doc=__doc__)
    c = CustomController(options, stdout=stdout)

    if options.args:
        c.onecmd(' '.join(options.args))

    if options.interactive:
        c.exec_cmdloop(args, options)


def run_supervisor_command_sync(command, *args):
    logger.debug('Running sync supervisor command: %s %s', command, args)
    stdout = BytesIO()
    supervisor_main(['-c', settings.get_supervisor_configuration_filename(), command] + list(args),
                    stdout=stdout)

    stdout.seek(0)
    return stdout.read().decode('utf-8')


def run_supervisor_command_async(command, args, delay_seconds=None, dev_null=False):
    logger.debug('Running async supervisor command: %s %s', command, args)
    shell_command = '{executable} -c {configuration_filename} {command} {args}'.format(
        executable=get_executable_path('supervisorctl'),
        configuration_filename=settings.get_supervisor_configuration_filename(),
        command=command,
        args=' '.join(args))
    run_command_async(shell_command, delay_seconds, dev_null=dev_null)


def run_supervisor_command(command, args, is_async=False, async_delay_seconds=None,
                           async_dev_null=False):
    if is_async:
        run_supervisor_command_async(command, args, delay_seconds=async_delay_seconds,
                                     dev_null=async_dev_null)
    else:
        return run_supervisor_command_sync(command, *args)
