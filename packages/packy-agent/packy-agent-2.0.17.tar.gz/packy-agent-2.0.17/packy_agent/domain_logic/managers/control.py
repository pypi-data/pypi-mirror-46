import os
import logging
import re
import time
import signal

from subprocess import call
from psutil import Process, NoSuchProcess

from packy_agent.utils.services.systemd import nginx_service
from packy_agent.utils.shell import run_command_async
from packy_agent.utils.platforms import is_inside_docker_container

from packy_agent.configuration.settings import settings
from packy_agent.utils.supervisor import run_supervisor_command
from packy_agent.domain_logic.constants import (
    WORKER_COMPONENT, CONSOLE_COMPONENT, WATCHDOG_COMPONENT, COMPONENTS)
from packy_agent.utils.shell import terminate_process, kill_process, reload_process

WORKER_SUPERVISOR_PROGRAM = WORKER_COMPONENT
CONSOLE_SUPERVISOR_PROGRAM = CONSOLE_COMPONENT
WATCHDOG_SUPERVISOR_PROGRAM = WATCHDOG_COMPONENT
NGINX_SUPERVISOR_PROGRAM = 'nginx'
SUPERVISOR_PROGRAMS = (
    WORKER_SUPERVISOR_PROGRAM, CONSOLE_SUPERVISOR_PROGRAM, WATCHDOG_SUPERVISOR_PROGRAM,
    NGINX_SUPERVISOR_PROGRAM)

COMPONENT_TO_SUPERVISOR_PROGRAM_MAP = {
    WORKER_COMPONENT: WORKER_SUPERVISOR_PROGRAM,
    CONSOLE_COMPONENT: CONSOLE_SUPERVISOR_PROGRAM,
    WATCHDOG_COMPONENT: WATCHDOG_SUPERVISOR_PROGRAM,
}
COMPONENT_TO_SUPERVISOR_PROGRAM_MAP_REVERSE = {
    v: k for k, v in COMPONENT_TO_SUPERVISOR_PROGRAM_MAP.items()}

STARTING = 'STARTING'
RUNNING = 'RUNNING'
STOPPING = 'STOPPING'
STOPPED = 'STOPPED'
STATUS_RE = r' +([A-Z]+)(.*)$'
PID_UPTIME_RE = re.compile('^ +pid (\d+), uptime (.*)$')

logger = logging.getLogger(__name__)


def resolve_target(target):
    supervisor_program = COMPONENT_TO_SUPERVISOR_PROGRAM_MAP.get(target)
    if supervisor_program:
        component = target
    else:
        supervisor_program = target
        component = None

    if supervisor_program not in SUPERVISOR_PROGRAMS:
        raise ValueError(f'Unknown supervisor program {supervisor_program}')

    if supervisor_program == NGINX_SUPERVISOR_PROGRAM and not is_inside_docker_container():
        supervisor_program = None
        service = nginx_service
    else:
        service = None

    return component, supervisor_program, service


def get_console_uwsgi_pid():
    pid_filename = settings.get_console_uwsgi()['pid_filename']
    try:
        with open(pid_filename) as f:
            return int(f.read())
    except Exception:
        logger.warning('Unable to get uWSGI pid')


def define_is_async_for_supervisor_program(is_async, supervisor_program):
    if is_async is None:
        component = COMPONENT_TO_SUPERVISOR_PROGRAM_MAP_REVERSE.get(supervisor_program)
        # Stopping itself is always async, unless explictly set otherwise
        is_async = component and component == settings.get_component()

    return is_async


def define_is_async_for_process(is_async, pid):
    if is_async is None:
        is_async = os.getpid() == pid

    return is_async


class ControlManager:

    def start(self, target, force=False):
        logger.info(f'STARTING {target}...')
        component, supervisor_program, service = resolve_target(target)

        if component == WORKER_COMPONENT:
            settings.set_worker_stopped(False)

        if not force and self.is_running(target):
            return

        if supervisor_program:
            run_supervisor_command('start', (supervisor_program,))
        elif service:
            service.start()
        else:
            raise ValueError(f'Unknown target: {target}')  # should never get here

    def kill_process(self, process, is_async=None):
        process_pid = process.pid
        logger.info('KILLING process: %s...', process_pid)
        is_async = define_is_async_for_process(is_async, process_pid)
        if is_async:
            if process.is_running():  # minimize chance of targeting reused PID
                kill_process(process_pid, is_async=True)
        else:
            try:
                process.kill()
            except NoSuchProcess:
                pass

    def terminate_process(self, process, is_async=None):
        process_pid = process.pid
        logger.info('TERMINATING process: %s...', process_pid)
        is_async = define_is_async_for_process(is_async, process_pid)
        if is_async:
            if process.is_running():  # minimize chance of targeting reused PID
                terminate_process(process_pid, is_async=True)
        else:
            try:
                process.terminate()
            except NoSuchProcess:
                pass

    def stop_supervisor_program(self, name, is_async=None, async_delay_seconds=None,
                                async_dev_null=False):
        logger.info('STOPPING supervisor program: %s...', name)
        is_async = define_is_async_for_supervisor_program(is_async, name)
        run_supervisor_command('stop', (name,), is_async=is_async,
                               async_delay_seconds=async_delay_seconds,
                               async_dev_null=async_dev_null)

    def stop(self, target, force=False, is_async=None, async_delay_seconds=None,
             async_dev_null=False, set_stopped=True):
        logger.info('STOPPING %s...', target)
        component, supervisor_program, service = resolve_target(target)

        if set_stopped and component == WORKER_COMPONENT:
            settings.set_worker_stopped(True)

        if not force and self.is_stopped(target):
            return

        # Get process before trying to stop it
        pid = self.get_pid(target)
        if pid is None:
            return  # was already stopped

        try:
            process = Process(pid)
        except NoSuchProcess:
            return  # was already stopped

        if supervisor_program:
            is_async = define_is_async_for_supervisor_program(is_async, supervisor_program)
            self.stop_supervisor_program(supervisor_program, is_async=is_async,
                                         async_delay_seconds=async_delay_seconds,
                                         async_dev_null=async_dev_null)
        elif service:
            is_async = define_is_async_for_process(is_async, pid)
            service.stop(is_async=is_async)
        else:
            raise ValueError(f'Unknown target: {target}')  # should never get here

        # if we are stopping ourself then we will die somewhere here, otherwise will wait until
        # other process will stop
        # we are not using self.is_running() because supervisor may auto-restart the process
        # we are good if original process is stopped even once

        check_period_seconds = settings.get_process_status_check_period_seconds()

        timeout_absolute = time.time() + settings.get_process_stop_timeout_seconds()
        if process.is_running() and time.time() < timeout_absolute:
            logger.debug('WAITING %s to stop', target)
            while process.is_running() and time.time() < timeout_absolute:
                time.sleep(check_period_seconds)  # expect to be patched by gevent when needed

        if process.is_running():
            logger.info('TERMINATING process of %s (pid: %s)...', target, pid)
            self.terminate_process(process, is_async=is_async)
        else:
            return

        timeout_absolute = time.time() + settings.get_sigterm_timeout_seconds()
        while process.is_running() and time.time() < timeout_absolute:
            time.sleep(check_period_seconds)  # expect to be patched by gevent when needed

        if process.is_running():
            logger.info('KILLING process of %s (pid: %s)...', target, pid)
            self.kill_process(process, is_async=is_async)
        else:
            logger.error('Could not stop process of %s (pid: %s)...', target, pid)

    def restart_supervisor_program(self, name, is_async=None, async_delay_seconds=None,
                                   async_dev_null=False):
        logger.info('RESTARTING supervisor program: %s...', name)
        is_async = define_is_async_for_supervisor_program(is_async, name)
        run_supervisor_command('restart', (name,), is_async=is_async,
                               async_delay_seconds=async_delay_seconds,
                               async_dev_null=async_dev_null)

    def restart(self, target, is_async=None, async_delay_seconds=None, async_dev_null=False):
        logger.info('RESTARTING %s...', target)
        component, supervisor_program, service = resolve_target(target)

        if component:
            settings.update_restarted_at_ts(component)

        if component == WORKER_SUPERVISOR_PROGRAM:
            settings.set_worker_stopped(False)

        # Get process before trying to stop it
        pid = self.get_pid(target)
        if pid is None and component == CONSOLE_COMPONENT:
            # One more chance to get PID for Console component
            pid = get_console_uwsgi_pid()

        process = None
        if pid is not None:
            try:
                process = Process(pid)
            except NoSuchProcess:
                pass

        if process is None:
            self.start(target)  # equivalent to restart because process is not running
            return
        else:
            if supervisor_program:
                is_async = define_is_async_for_supervisor_program(is_async, supervisor_program)
                if component == CONSOLE_COMPONENT:
                    logger.debug('RELOADING %s (pid: %s)', component, pid)
                    if is_async:
                        reload_process(pid, is_async=True, async_delay_seconds=async_delay_seconds,
                                       async_dev_null=async_dev_null)
                    else:
                        try:
                            process.send_signal(signal.SIGHUP)
                        except NoSuchProcess:
                            pass

                    # TODO(dmu) MEDIUM: Somehow validate that uWSGI has actually reloaded
                    return  # PID does not change on uWSGI reload, so just return

                    # `uwsgi.reload()` breaks current request and we do not manage to send
                    # response to user
                    # Restart via supervisor does not work properly under Docker, because
                    # supervisord under Docker kills background subprocess that runs
                    # restart procedure (maybe it is Alpine specific)
                else:
                    self.restart_supervisor_program(supervisor_program, is_async=is_async,
                                                    async_delay_seconds=async_delay_seconds,
                                                    async_dev_null=async_dev_null)

            elif service:
                service.restart()
            else:
                raise ValueError(f'Unknown target: {target}')  # should never get here

        check_period_seconds = settings.get_process_status_check_period_seconds()

        timeout_absolute = time.time() + settings.get_process_restart_timeout_seconds()
        while process.is_running() and time.time() < timeout_absolute:
            time.sleep(check_period_seconds)  # expect to be patched by gevent when needed

        if process.is_running():
            logger.warning('Could not do regular restart of %s (pid: %s)...', target, pid)
            logger.info('STOPPING %s (pid: %s)...', target, pid)
            is_async = define_is_async_for_process(is_async, pid)
            self.stop(target, is_async=is_async, async_delay_seconds=async_delay_seconds,
                      async_dev_null=async_dev_null, set_stopped=False)
            if process.is_running():
                logger.warning('Could not stop %s (pid: %s)...', target, pid)
                return
            else:
                logger.info('STARTING %s...', target)
                self.start(target)

    def restart_all(self, delay_seconds=None):
        logger.info('Restarting all components...')
        calling_component = settings.get_component()
        components = list(COMPONENTS)
        components.remove(calling_component)
        components.append(NGINX_SUPERVISOR_PROGRAM)

        for component in components:
            self.restart(component)

        # it is important that calling component is the last to be restarted
        self.restart(calling_component, async_delay_seconds=delay_seconds)
        # TODO(dmu) MEDIUM: Restart via supervisor does not work properly under Docker, because
        #                   supervisord under Docker kills background subprocess that runs
        #                   restart procedure (maybe it is Alpine specific)
        # run_supervisor_command('restart', ('all',), delay_seconds=delay_seconds)

    def get_status(self, target):
        logger.debug('GETTING status for %s', target)
        _, supervisor_program, service = resolve_target(target)

        status = pid = uptime = None

        if supervisor_program:
            logger.debug('GETTING status of Supervisor program: %s', supervisor_program)
            output = run_supervisor_command('status', (supervisor_program,)).rstrip()
            status_re = re.compile('^' + supervisor_program + STATUS_RE)
            match_status = status_re.match(output)
            if match_status:
                status, tail = match_status.groups()
                match_pid_uptime = PID_UPTIME_RE.match(tail)
                if match_pid_uptime:
                    pid, uptime = match_pid_uptime.groups()
                    pid = int(pid)
        elif service:
            # TODO(dmu) LOW: Should we use abstract statuses instead of resembling supervisor
            #                statuses
            logger.debug('GETTING status of a service: %s', service)
            status = RUNNING if service.is_running() else STOPPED
            pid = service.get_pid()
            # TODO(dmu) LOW: Support uptime for services (uptime package can be used)
        else:
            raise ValueError(f'Unknown target: {target}')  # should never get here

        logger.debug('GOT status: %s, %s, %s', status, pid, uptime)
        return status, pid, uptime

    def get_worker_status_line(self):
        status, _, uptime = self.get_status(WORKER_COMPONENT)
        worker_status_line = status or 'UNKNOWN'
        if uptime:
            worker_status_line += f' (uptime {uptime})'

        return worker_status_line

    def is_running(self, target):
        status, _, _ = self.get_status(target)
        return status == RUNNING

    def is_starting(self, target):
        status, _, _ = self.get_status(target)
        return status == STARTING

    def is_stopping(self, target):
        status, _, _ = self.get_status(target)
        return status == STOPPING

    def is_stopped(self, target):
        status, _, _ = self.get_status(target)
        return status == STOPPED

    def get_pid(self, target):
        _, pid, _ = self.get_status(target)
        return pid

    def reboot(self, delay_seconds=None, change_worker_stopped_status=True):
        settings.reset_network_data_usage()
        settings.update_rebooted_at_ts(delta=delay_seconds or 0)
        if change_worker_stopped_status:
            settings.set_worker_stopped(False)

        if not settings.is_reboot_enabled():
            logger.info('Reboot was disabled (for developer protection)')
            return

        if is_inside_docker_container():
            command = ['killall', 'supervisord']
        else:
            command = ['reboot', 'now']

        if delay_seconds is None:
            call(command)
        else:
            run_command_async(' '.join(command), delay_seconds=delay_seconds)


# As long as manager is stateless object we do not need to care about greenlet-multitasking safety
control_manager = ControlManager()
