import logging
from collections import deque
from abc import abstractmethod, ABC
import time


ITERATION_LOG_MAX_LEN = 100

logger = logging.getLogger(__name__)


class Loop(ABC):

    formal_name = None
    loop_type = 'base'

    def __init__(self, is_safe_iteration=True, is_logged_iteration=True):
        self.is_safe_iteration = is_safe_iteration
        self.is_logged_iteration = is_logged_iteration

        self.counter = 0

        self.iteration_log = deque(maxlen=ITERATION_LOG_MAX_LEN)

    @abstractmethod
    def iteration(self):
        raise NotImplementedError('Method must be implemented in child class')

    def iteration_wrapper(self):
        self.iteration_log.clear()

        description = self.description
        if self.is_logged_iteration:
            logger.debug(f'STARTED iteration: {description}')

        start_time = time.time()
        try:
            self.iteration()
        except Exception:
            elapsed = time.time() - start_time
            if self.is_safe_iteration:
                logger.exception(f'ERROR during iteration (in {elapsed:.6g}s): {description}')
            else:
                raise
        else:
            elapsed = time.time() - start_time
            if self.is_logged_iteration:
                logger.debug(f'FINISHED iteration (in {elapsed:.6g}s): {description}')
        finally:
            self.counter += 1

    def loop(self):
        logger.debug(f'STARTED {self.description}')
        while True:
            self.iteration_wrapper()

    def collect_log(self, message):
        self.iteration_log.append((time.time(), message))
        logger.debug('Collecting log message: %s', message)

    @property
    def description(self):
        return self.__class__.__name__
