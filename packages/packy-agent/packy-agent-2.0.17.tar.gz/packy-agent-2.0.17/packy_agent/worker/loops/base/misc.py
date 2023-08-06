import logging

from itertools import chain
from abc import ABC

from packy_agent.worker.loops.base.startable import StartableLoop
from packy_agent.worker.loops.base.stoppable import StoppableLoop
from packy_agent.exceptions import ImproperlyConfiguredError


logger = logging.getLogger(__name__)


def describe_callable(callable_, args, kwargs):
    return '{}({})'.format(
        callable_.__name__,
        ', '.join(chain(map(repr, args), (f'{k}={v !r}' for k, v in kwargs.items()))))


class StartableStoppableLoop(StoppableLoop, StartableLoop, ABC):

    loop_type = 'startable_stoppable'


class CallableLoop(StartableStoppableLoop, ABC):

    loop_type = 'callable'

    def __init__(self, callable_=None, args=(), kwargs=None, is_safe_iteration=True,
                 is_logged_iteration=True, **mkwargs):
        super().__init__(is_safe_iteration=is_safe_iteration,
                         is_logged_iteration=is_logged_iteration, **mkwargs)

        self.callable = callable_
        self.args = args
        self.kwargs = kwargs or {}

    def call(self):
        if self.callable:
            logger.info(f'STARTED actual work: {self.description}')
            result = self.callable(*self.args, **self.kwargs)
            logger.info(f'FINISHED actual work: {self.description}')
        else:
            raise ImproperlyConfiguredError("Provide callable or override 'call' method")

        return result
