import time
import logging

from packy_agent.utils.datetime import get_croniter
from packy_agent.worker.loops.base.misc import CallableLoop, describe_callable
from packy_agent.exceptions import ImproperlyConfiguredError


logger = logging.getLogger(__name__)


class ScheduledLoop(CallableLoop):

    loop_type = 'scheduled'

    def __init__(self, schedule=None, callable_=None, args=(), kwargs=None, is_safe_iteration=True,
                 is_logged_iteration=True, **mkwargs):
        super().__init__(callable_=callable_, args=args, kwargs=kwargs,
                         is_safe_iteration=is_safe_iteration,
                         is_logged_iteration=is_logged_iteration, **mkwargs)

        if not schedule:
            raise ImproperlyConfiguredError('Schedule must be provided')

        self.schedule = schedule

        self.croniter = None

    def iteration(self):
        task_description = self.description

        next_moment = self.croniter.get_next()
        current_moment = time.time()
        if next_moment >= current_moment:
            wait_time = next_moment - current_moment
            if wait_time > 0:
                logger.debug(f'WAITING {wait_time:.6g} seconds for next '
                             f'iteration of {task_description} at {next_moment}')
                self.sleep(wait_time)

            self.call()
        else:
            missed_seconds = current_moment - next_moment
            logger.warning(f'MISSED %.1f epoch moment for %s (%.3f seconds late)',
                           next_moment, task_description, missed_seconds)
            # roll croniter
            while next_moment < current_moment:
                next_moment = self.croniter.get_next()
                self.sleep(0.01)  # avoid being CPU-bound

    def loop(self):
        self.croniter = get_croniter(self.schedule)
        super().loop()

    @property
    def description(self):
        return describe_callable(self.callable or self.__class__.__name__,
                                 self.args, self.kwargs) + f' ({self.schedule})'
