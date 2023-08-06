from abc import ABC
import logging

from gevent.event import Event

from packy_agent.worker.loops.base.loop import Loop


logger = logging.getLogger(__name__)


class StoppableLoop(Loop, ABC):

    loop_type = 'stoppable'

    def __init__(self, is_safe_iteration=True, is_logged_iteration=True):
        super().__init__(is_safe_iteration=is_safe_iteration,
                         is_logged_iteration=is_logged_iteration)
        self.is_running = False
        self.is_stopping = False
        self.wake_up_event = Event()

    def loop(self):
        self.is_running = True
        self.is_stopping = False
        logger.debug(f'STARTED {self.description}')

        while self.is_running:
            self.iteration_wrapper()
            if self.is_stopping:
                break

        self.is_running = False
        self.is_stopping = False
        logger.debug(f'STOPPED {self.description}')

    def sleep(self, timeout):
        self.wake_up_event.clear()
        self.wake_up_event.wait(timeout)

    def stop(self):
        logger.debug(f'STOP requested for {self.description}')
        self.is_stopping = True
        self.wake_up_event.set()
