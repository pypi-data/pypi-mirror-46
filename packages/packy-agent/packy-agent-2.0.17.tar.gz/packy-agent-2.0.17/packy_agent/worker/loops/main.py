import logging

from packy_agent.constants import PING_MODULE, TRACE_MODULE, SPEEDTEST_MODULE, HTTP_MODULE
from packy_agent.configuration.settings import settings
from packy_agent.worker.loops.task_results.consumer import TaskResultsConsumer
from packy_agent.worker.loops.task_results.submitter import TaskResultsSubmitter
from packy_agent.worker.loops.task_results.purger import TaskResultsPurger
from packy_agent.worker.loops.management.communication import PackyCommunicationLoop
from packy_agent.worker.loops.management.heartbeat import HeartbeatLoop
from packy_agent.worker.loops.management.guard import GuardLoop
from packy_agent.worker.loops.management.status import StatusLoop
from packy_agent.worker.loops.modules.ping import PingTaskLoop
from packy_agent.worker.loops.modules.traceroute import TracerouteTaskLoop
from packy_agent.worker.loops.modules.speedtest import SpeedtestTaskLoop
from packy_agent.worker.loops.modules.http import HTTPTaskLoop


MODULE_NAME_TO_LOOP_MAP = {
    PING_MODULE: PingTaskLoop,
    TRACE_MODULE: TracerouteTaskLoop,
    SPEEDTEST_MODULE: SpeedtestTaskLoop,
    HTTP_MODULE: HTTPTaskLoop,
}

logger = logging.getLogger(__name__)


class MainLoop:

    def __init__(self, task_definitions=None):
        # TODO(dmu) HIGH: We should not get task at initialization only. Instead we should
        #                 track changes (we have Packy Communication event for this) and add/remove
        #                 them on fly
        self.task_definitions = task_definitions or settings.get_tasks() or ()

        self.is_running = False
        self.is_stopping = False
        self.tasks = []

        self.task_results_consumer = None
        self.task_results_submitter = None
        self.task_results_purger = None

        self.communication_loop = None
        self.heartbeat_loop = None
        self.guard_loop = None
        self.status_loop = None

        self.loops = []

    def _start_loop(self, loop):
        if loop:
            loop.start()
            self.loops.append(loop)

    def _join_loops(self):
        for loop in self.loops:
            loop.join()

    def _stop_loops(self):
        for loop in self.loops:
            loop.stop()

    def run(self):
        if self.is_running:
            return

        self.is_running = True
        self.is_stopping = False
        logger.debug('STARTED main loop')

        active_loops = settings.get_worker_loops()

        if TaskResultsConsumer.formal_name in active_loops:
            self.task_results_consumer = TaskResultsConsumer()

        if TaskResultsSubmitter.formal_name in active_loops:
            self.task_results_submitter = TaskResultsSubmitter()

        if TaskResultsPurger.formal_name in active_loops:
            self.task_results_purger = TaskResultsPurger()

        if PackyCommunicationLoop.formal_name in active_loops:
            self.communication_loop = PackyCommunicationLoop(
                period=settings.get_worker_packy_communication_retry_period())

        if HeartbeatLoop.formal_name in active_loops:
            self.heartbeat_loop = HeartbeatLoop(
                period=settings.get_worker_heartbeat_period_seconds())

        if GuardLoop.formal_name in active_loops:
            self.guard_loop = GuardLoop(period=settings.get_worker_guard_period_seconds())

        if StatusLoop.formal_name in active_loops:
            self.status_loop = StatusLoop(self,
                                          address=settings.get_worker_http_bind_address(),
                                          port=settings.get_worker_http_port())

        if self.task_results_consumer:
            inbound_queue = self.task_results_consumer.inbound_queue
        else:
            inbound_queue = None

        tasks = []
        for td in self.task_definitions:
            module_name = td['module_name']
            loop = MODULE_NAME_TO_LOOP_MAP.get(module_name)
            if not loop:
                logger.debug('Unsupported module: %s', module_name)
                continue

            if loop.formal_name not in active_loops:
                continue

            tasks.append(
                loop(schedule=td['schedule'], args=td.get('args') or (),
                     kwargs=td.get('kwargs') or {},
                     outbound_queue=inbound_queue))

        self.tasks = tasks

        for task in self.tasks:
            self._start_loop(task)
        self._start_loop(self.task_results_consumer)
        self._start_loop(self.task_results_submitter)
        self._start_loop(self.task_results_purger)
        self._start_loop(self.communication_loop)
        self._start_loop(self.heartbeat_loop)
        self._start_loop(self.guard_loop)
        self._start_loop(self.status_loop)

        self._join_loops()

        self.is_running = False
        self.is_stopping = False
        logger.debug('STOPPED main loop')

    def stop(self):
        logger.debug('STOP requested for main loop')
        self.is_stopping = True
        self._stop_loops()
