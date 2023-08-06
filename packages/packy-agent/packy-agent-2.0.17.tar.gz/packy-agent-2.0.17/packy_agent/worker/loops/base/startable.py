import logging
from abc import ABC

import gevent

from packy_agent.worker.loops.base.loop import Loop


logger = logging.getLogger(__name__)


class StartableLoop(Loop, ABC):

    loop_type = 'startable'

    def __init__(self, is_safe_iteration=True, is_logged_iteration=True):
        super().__init__(is_safe_iteration=is_safe_iteration,
                         is_logged_iteration=is_logged_iteration)
        self.greenlet = None
        self.is_started = False

    def get_greenlet(self):
        return self.greenlet

    def start(self):
        if self.is_started:
            return

        self.greenlet = gevent.Greenlet(self.loop)
        self.greenlet.start()
        self.is_started = True

    def join(self):
        self.greenlet.join()
