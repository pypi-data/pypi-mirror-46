import os
import time
import logging
from collections import defaultdict, OrderedDict
from threading import Condition

from psutil import Process, NoSuchProcess, cpu_percent, cpu_count
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError, HTTPError
from sentry_sdk import capture_message, capture_exception

from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.constants import (
    WORKER_COMPONENT, CONSOLE_COMPONENT, WATCHDOG_COMPONENT)
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.clients.packy_agent_worker import get_packy_agent_worker_client
from packy_agent.constants import MODULE_LOOP_SUFFIX
from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.utils.datetime import get_croniter
from packy_agent.domain_logic.managers.control import NGINX_SUPERVISOR_PROGRAM as NGINX
from packy_agent.utils.fs import get_available_disk_space


logger = logging.getLogger(__name__)


DAY_SECONDS = 60 * 60 * 24
MESSAGE_KEY_LEN = 10
MAX_THROTTLE_DICT_SIZE = 1024
FAILOVER_CHECK_PERIOD_SECONDS = 30
ROOT_PID = 1
START = 'start'
RESTART = 'restart'
REBOOT = 'reboot'
ERROR = 'error'
WARNING = 'warning'
UNKNOWN = 'unknown'
OK = 'ok'


def get_loop_deadline(loop_props):
    now_ts = time.time()
    loop_type = loop_props.get('loop_type')
    if loop_type in ('scheduled', 'scheduled_producer'):
        schedule = loop_props.get('schedule')
        if schedule:
            croniter = get_croniter(schedule)
            croniter.get_next()  # include one full iteration at least (so we get warned only if iterations tend to overlap)
            return croniter.get_next()
    elif loop_type == 'periodic':
        period = loop_props.get('period')
        if period is not None:
            return now_ts + period + settings.get_watchdog_relax_period_seconds()


def is_uptime_gte(component, duration):
    started_at_ts = settings.get_subkey(component, 'started_at_ts')
    return started_at_ts is not None and time.time() - started_at_ts >= duration


class WatchdogService:

    def __init__(self, raven_client=None):
        self.raven_client = raven_client

        self._graceful_stop = False
        self.condition = Condition()

        self.known_activated_time = None
        self.last_restart_time = None
        self.last_known_online_time = None

        self.last_known_online_ts = None

        self.has_reported_not_activated = False
        self.has_reported_stopped = False

        self.collected_counter = None
        self.collected_counter_ts = None
        self.collected_counter_deadline_ts = None
        self.submitted_counter = None
        self.submitted_counter_ts = None
        self.submitted_counter_deadline_ts = None
        self.purged_records = None
        self.purged_records_ts = None

        self.loop_stats = defaultdict(dict)

        self.report_throttle = OrderedDict()

    def graceful_stop(self):
        self._graceful_stop = True
        with self.condition:
            self.condition.notify_all()

    def throttle(self, message, period):
        now_ts = time.time()

        message_key = message[:MESSAGE_KEY_LEN]
        last_reported_ts = self.report_throttle.get(message_key)
        if last_reported_ts and time.time() < last_reported_ts + period:
            logger.debug('Message has been throttled: %s', message)
            return True
        else:
            self.report_throttle[message_key] = now_ts
            if len(self.report_throttle) > MAX_THROTTLE_DICT_SIZE:
                self.report_throttle.popitem(last=False)
            return False

    def report_warning(self, message):
        logger.warning(message)
        if not self.throttle(message, settings.get_watchdog_warning_report_period()):
            capture_message(message, level='warning')

    def report_error(self, message):
        logger.error(message)
        if not self.throttle(message, settings.get_watchdog_error_report_period()):
            capture_message(message, level='error')

    def report_with_perf_info(self, message):
        message += ' (load average: {}, CPU: {:.1f}%, CPUs: {})'.format(
            ', '.join('{:.3g}'.format(v) for v in os.getloadavg()), cpu_percent(), cpu_count())
        self.report_warning(message)

    def start_worker(self):
        self.report_warning('Watchdog requested Worker start')
        control_manager.start(WORKER_COMPONENT)

    def restart_component(self, component):
        restart_min_period_seconds = settings.get_restart_min_period_seconds()
        restarted_at_ts = settings.get_subkey(component, 'restarted_at_ts')
        if (restarted_at_ts is not None and
                time.time() - restarted_at_ts < restart_min_period_seconds):
            logger.debug(f'Restart is requested for {component.capitalize()} again too soon')
        else:
            self.report_warning(f'Watchdog requested {component.capitalize()} restart')
            control_manager.restart(component)

            # TODO(dmu) LOW: Should we restart nginx inside `control_manager.restart()`?
            if component == CONSOLE_COMPONENT:
                control_manager.restart(NGINX)

    def restart_console(self):
        self.restart_component(CONSOLE_COMPONENT)

    def restart_worker(self):
        self.restart_component(WORKER_COMPONENT)

    def restart_watchdog(self):
        self.restart_component(WATCHDOG_COMPONENT)

    def reboot(self):
        reboot_min_period_seconds = settings.get_reboot_min_period_seconds()
        rebooted_at_ts = settings.get_rebooted_at_ts()
        if (rebooted_at_ts is not None and
                time.time() - rebooted_at_ts < reboot_min_period_seconds):
            logger.debug('Reboot is requested again too soon')
        else:
            self.report_warning('Watchdog requested reboot')
            control_manager.reboot()

    def resolve_online_status(self):
        logger.debug('Resolving agent online status...')
        now_ts = time.time()

        if not settings.get_worker_heartbeat_enabled():
            logger.debug('Heartbeat is disabled, so we do not expect agent to be online')
            return

        try:
            is_online = get_packy_server_client().is_agent_online()
        except Exception:
            logger.debug('Could not get agent online status. Maybe Packy Server is not available')
            return

        if is_online is None:
            logger.debug('Could not get agent online status. Maybe there is an issue with '
                         'Packy Server')
            return
        elif is_online:
            self.last_known_online_ts = now_ts

        if self.last_known_online_ts is None:
            return
        else:
            offline_period_seconds = now_ts - self.last_known_online_ts

            # If we have been offline long enough and rebooted long ago then go reboot
            if (offline_period_seconds >= settings.get_worker_offline_to_reboot_seconds() and
                    now_ts >= (settings.get_rebooted_at_ts() or 0) +
                               settings.get_worker_reboot_wait_seconds()):
                return REBOOT
            # If we have been offline long enough and started long ago then go restart
            elif (offline_period_seconds >= settings.get_worker_offline_to_restart_seconds() and
                  now_ts >= (max(settings.get_worker_started_at_ts() or 0,
                                 settings.get_worker_restarted_at_ts() or 0)) +
                             settings.get_worker_restart_wait_seconds()):
                return RESTART

    def resolve_worker_supervisor_program_status(self):
        logger.debug('Resolving Worker running status (supervisor)...')
        if control_manager.is_running(WORKER_COMPONENT):
            logger.debug('Worker is running (supervisor)')
            return
        elif not (control_manager.is_starting(WORKER_COMPONENT) or
                  control_manager.is_stopping(WORKER_COMPONENT)):
            logger.debug('Worker is NOT running (supervisor)')
            return START

    def resolve_worker_process_status(self):
        pid = control_manager.get_pid(WORKER_COMPONENT)

        try:
            Process(pid)
            return
        except NoSuchProcess:
            return RESTART

    def resolve_loops_activity(self, loops):
        now_ts = time.time()

        for loop_name, loop_props in loops.items():
            new_counter = loop_props.get('counter')
            current_counter = (self.loop_stats.get(loop_name) or {}).get('counter')
            if new_counter == current_counter:
                change_deadline_ts = self.loop_stats[loop_name].get('change_deadline_ts')
                if change_deadline_ts is not None and now_ts > change_deadline_ts:
                    counter_ts = self.loop_stats[loop_name].get('counter_ts')
                    self.report_with_perf_info(
                        f'{loop_name} counter is stale on {current_counter} at '
                        f'{counter_ts:.3f} (change expected before '
                        f'{change_deadline_ts:.3f})')
                    self.loop_stats[loop_name]['change_deadline_ts'] = get_loop_deadline(loop_props)
            else:
                self.loop_stats[loop_name]['counter'] = new_counter
                self.loop_stats[loop_name]['counter_ts'] = now_ts

                logger.debug('%s updated counter from %s to %s at %.3f', loop_name,
                             current_counter, new_counter, now_ts)

                self.loop_stats[loop_name][
                    'change_deadline_ts'] = get_loop_deadline(loop_props)

    def resolve_workflow(self, status):

        # Filter out measurement loops
        running_measurement_loops = {k: v for k, v in (status.get('loops') or {}).items()
                                     if k.endswith(MODULE_LOOP_SUFFIX)}
        if not running_measurement_loops:
            logger.debug('No active measurement loops found')
            return  # No measurement loops, so we should not expect counters increment

        deadline_ts = min(
            list(filter(None, (get_loop_deadline(loop_props) for loop_name, loop_props
                               in running_measurement_loops.items()))) or (None,))
        logger.debug('Workflow deadline is calculated as %s', deadline_ts)

        relax_period = settings.get_watchdog_relax_period_seconds()
        now_ts = time.time()

        collected_counter = status.get('collected_counter')
        if self.collected_counter == collected_counter:
            logger.debug('Collected counter did not change (value: %s)', self.collected_counter)
            if (self.collected_counter_deadline_ts and
                    now_ts >= (self.collected_counter_deadline_ts + relax_period)):
                self.report_with_perf_info(f'Measurement collection is stale on {self.collected_counter} '
                                  f'at {self.collected_counter_ts:.3f}')
                self.collected_counter_deadline_ts = deadline_ts
        else:
            self.collected_counter = collected_counter
            self.collected_counter_ts = now_ts
            self.collected_counter_deadline_ts = deadline_ts

        submitted_counter = status.get('submitted_counter')
        if self.submitted_counter == submitted_counter:
            logger.debug('Submitted counter did not change (value: %s)', self.submitted_counter)
            if (self.submitted_counter_deadline_ts and
                    now_ts >= self.submitted_counter_deadline_ts + relax_period):
                self.report_with_perf_info(f'Measurement submission is stale on {self.submitted_counter} '
                                  f'at {self.submitted_counter_ts:.3f}')
                self.submitted_counter_deadline_ts = deadline_ts
        else:
            self.submitted_counter = submitted_counter
            self.submitted_counter_ts = now_ts
            self.submitted_counter_deadline_ts = deadline_ts

        purged_records = status.get('purged_records')
        if self.purged_records == purged_records:
            purge_period = settings.get_worker_purge_period_seconds() + relax_period
            if self.purged_records_ts and now_ts >= self.purged_records_ts + purge_period:
                self.report_with_perf_info(f'Measurement purging is stale on {self.purged_records} '
                                  f'at {self.purged_records_ts:.3f}')

        else:
            self.purged_records = purged_records
            self.purged_records_ts = now_ts

    def resolve_worker_response(self):
        start = time.time()
        try:
            status = get_packy_agent_worker_client().get_status()
            finish = time.time()
        except RequestsConnectionError:
            logger.debug('Could not get Worker status over HTTP')
            return RESTART
        except HTTPError as ex:
            self.report_error(f'Packy Agent Worker returned HTTP{ex.response.status_code}: {ex!r}')
            return

        actual_duration = finish - start
        expected_duration = settings.get_worker_expected_http_response_time_seconds()
        if actual_duration > expected_duration:
            self.report_with_perf_info(
                f'It took {actual_duration:.3g} seconds for Packy Agent Worker '
                f'to respond while it was expected to take only '
                f'{expected_duration:.3g}')

        loops = status.get('loops')
        if loops:
            self.resolve_loops_activity(loops)
        else:
            self.report_warning('Worker did not return running loops')

        self.resolve_workflow(status)

    def handle_console(self):
        if is_uptime_gte(CONSOLE_COMPONENT, DAY_SECONDS):
            self.restart_console()
            return

        console_base_url = settings.get_console_base_url()
        try:
            response = requests.get(console_base_url)
        except RequestsConnectionError:
            self.restart_console()
            return
        else:
            if response.status_code != 200:
                self.restart_console()
                return

    def get_worker_action(self):
        if not settings.is_activated():
            if not self.has_reported_not_activated:
                self.has_reported_not_activated = True
                logger.info('Worker is not activated')

            return
        self.has_reported_not_activated = False

        if settings.is_worker_stopped():
            if not self.has_reported_stopped:
                self.has_reported_stopped = True
                logger.info('Worker is stopped on purpose')

            return
        self.has_reported_stopped = False

        for method in (self.resolve_online_status, self.resolve_worker_supervisor_program_status,
                       self.resolve_worker_process_status, self.resolve_worker_response):
            action = method()
            if action:
                return action

        if is_uptime_gte(WORKER_COMPONENT, DAY_SECONDS):
            return RESTART

    def handle_worker(self):
        action = self.get_worker_action()
        if action:
            logger.debug('Action is required for Worker: %s', action)
            if action == RESTART:
                self.restart_worker()
            elif action == START:
                self.start_worker()
            elif action == REBOOT:
                self.reboot()
        else:
            logger.debug('No action is required for worker')

    def handle_watchdog(self):
        if is_uptime_gte(WATCHDOG_COMPONENT, DAY_SECONDS):
            self.restart_watchdog()

    def handle_general(self):
        minimum_disk_space_bytes = settings.get_minimum_disk_space_bytes()
        available_disk_space = get_available_disk_space()
        if available_disk_space < minimum_disk_space_bytes:
            self.report_warning(f'Less than {minimum_disk_space_bytes} bytes of disk space is '
                                f'remaining: {available_disk_space} bytes')

    def loop_iteration(self):
        if (time.time() - settings.get_watchdog_started_at_ts() <
                settings.get_watchdog_warmup_period_seconds()):
            logger.debug('Warming up...')
            return

        try:
            self.handle_general()
        except Exception:
            logger.exception('Error during general handling')
            capture_exception()

        try:
            self.handle_worker()
        except Exception:
            logger.exception('Error while handling Worker')
            capture_exception()

        try:
            self.handle_console()
        except Exception:
            logger.exception('Error while handling Console')
            capture_exception()

        try:
            self.handle_watchdog()
        except Exception:
            logger.exception('Error while handling Watchdog')
            capture_exception()

    def run(self):
        logger.info('STARTED Watchdog')
        while not self._graceful_stop:
            start = time.time()
            try:
                self.loop_iteration()
            except Exception:
                logger.exception('Error during loop iteration')
                capture_exception()

            # Configuration may change with time, so we reread it every loop
            try:
                check_period_seconds = settings.get_watchdog_check_period_seconds()
            except Exception:
                check_period_seconds = FAILOVER_CHECK_PERIOD_SECONDS
                logger.exception('Could not get check period seconds from configuration file, '
                                 'using failover value: %s', check_period_seconds)
                capture_exception()

            wait_duration = check_period_seconds - (time.time() - start)
            if wait_duration > 0:
                logger.debug('Waiting for %.3g seconds for next iteration', wait_duration)
                with self.condition:
                    self.condition.wait(wait_duration)

        logger.info('STOPPED Watchdog gracefully')
