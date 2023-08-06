import logging
import os
import subprocess
import signal


logger = logging.getLogger(__name__)


def run_command_sync(command, raise_exception=False):
    logger.info('Started sync shell command: %s', command)
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as ex:
        logger.error('Sync shell command failed: %s: %s', command, ex.output.strip())
        if raise_exception:
            raise
    else:
        logger.info('Sync shell command succeeded: %s: %s', command, output.strip())
        return output


def run_command_async(command, delay_seconds=None, dev_null=False):
    if delay_seconds is not None:
        command = f'sleep {delay_seconds}; {command}'

    command = f'({command}) &'

    if dev_null:
        command = f'({command}) > /dev/null 2>&1'

    logger.debug('Started async shell command: %s', command)
    os.system(command)
    logger.debug('Finished async shell command: %s', command)


def run_command(command, is_async=False, raise_exception=False, async_delay_seconds=None,
                async_dev_null=False):
    logger.info('RUNNING shell command: %s', command)
    if is_async:
        run_command_async(command, delay_seconds=async_delay_seconds, dev_null=async_dev_null)
    else:
        return run_command_sync(command, raise_exception=raise_exception)


def send_signal(pid, signal_no, is_async=False, async_delay_seconds=None,
                async_dev_null=False):
    if is_async:
        run_command(f'kill -{signal_no} {pid}', is_async=True,
                    async_delay_seconds=async_delay_seconds, async_dev_null=async_dev_null)
    else:
        os.kill(pid,  signal_no)


def reload_process(pid, is_async=False, async_delay_seconds=None, async_dev_null=False):
    send_signal(pid, signal.SIGHUP, is_async=is_async,
                async_delay_seconds=async_delay_seconds, async_dev_null=async_dev_null)


def terminate_process(pid, is_async=False, async_delay_seconds=None, async_dev_null=False):
    send_signal(pid, signal.SIGTERM, is_async=is_async,
                async_delay_seconds=async_delay_seconds, async_dev_null=async_dev_null)


def kill_process(pid, is_async=False, async_delay_seconds=None, async_dev_null=False):
    send_signal(pid, signal.SIGKILL, is_async=is_async,
                async_delay_seconds=async_delay_seconds, async_dev_null=async_dev_null)
