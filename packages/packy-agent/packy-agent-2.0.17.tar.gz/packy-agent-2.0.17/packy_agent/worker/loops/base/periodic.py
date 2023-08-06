import time
import logging
from random import random

from packy_agent.worker.loops.base.misc import CallableLoop, describe_callable
from packy_agent.configuration.settings import settings


logger = logging.getLogger(__name__)


class PeriodicLoop(CallableLoop):

    loop_type = 'periodic'

    def __init__(self, period, callable_=None, args=(), kwargs=None,
                 is_logged_iteration=True, jitter_factor=None, **mkwargs):
        super().__init__(callable_=callable_, args=args, kwargs=kwargs,
                         is_safe_iteration=False,
                         is_logged_iteration=is_logged_iteration, **mkwargs)

        self.period = period
        if jitter_factor is None:
            self.jitter_factor = settings.get_worker_periodic_task_jitter_factor()
        else:
            self.jitter_factor = jitter_factor

    def iteration(self):
        self.call()

    def iteration_wrapper(self):
        description = self.description
        start_time = time.time()

        jitter_factor = self.jitter_factor
        period = self.period * (1 - jitter_factor + 2 * jitter_factor * random())

        try:
            super().iteration_wrapper()
        except Exception:
            elapsed = time.time() - start_time
            logger.exception(f'EXCEPTION in {description} job in {elapsed:.6g}s')
        else:
            elapsed = time.time() - start_time
            logger.info(f'DONE {description} job in {elapsed:.6g}s')

        if elapsed < period:
            wait_time = period - elapsed
            logger.debug(f'WAITING {wait_time:.6g}s for next iteration of {description}')
            self.sleep(wait_time)
        elif elapsed > period:
            longer = elapsed - period
            logger.warning(f'NOT WAITING {description} for next iteration: '
                           f'job took {longer:.6g}s longer than period ({period:.6g} seconds)')

    @property
    def description(self):
        if self.callable:
            part1 = describe_callable(self.callable, self.args, self.kwargs)
        else:
            part1 = self.__class__.__name__

        return f'{part1} (every {self.period}s)'
