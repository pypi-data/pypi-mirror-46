import logging
from abc import ABC

from gevent.queue import Queue

from packy_agent.worker.loops.base.misc import CallableLoop

logger = logging.getLogger(__name__)


class ProducerLoop(CallableLoop, ABC):

    loop_type = 'producer'

    def __init__(self, callable_=None, args=(), kwargs=None, is_safe_iteration=True,
                 is_logged_iteration=True, outbound_queue=None, **mkwargs):
        super().__init__(callable_=callable_, args=args, kwargs=kwargs,
                         is_safe_iteration=is_safe_iteration,
                         is_logged_iteration=is_logged_iteration, **mkwargs)

        self.produced_counter = 0
        self.outbound_queue = outbound_queue

    def call(self):
        logger.info('STARTED actual work: %s', self.description)
        result = self.callable(*self.args, **self.kwargs)
        logger.info('FINISHED actual work: %s', self.description)
        if result is None:
            logger.debug('Did not get result for %s', self.description)
        else:
            if self.outbound_queue:
                self.outbound_queue.put(result)

            self.produced_counter += 1

        return result
