from abc import ABC

from gevent.queue import Queue, Empty


from packy_agent.configuration.settings import settings
from packy_agent.worker.loops.base.misc import StartableStoppableLoop
from packy_agent.exceptions import ImproperlyConfiguredError


class ConsumerLoop(StartableStoppableLoop, ABC):

    def __init__(self, inbound_queue=None, callable_=None, timeout=None):
        super().__init__()
        self.inbound_queue = inbound_queue or Queue()
        self.callable = callable_
        self.timeout = timeout or settings.get_worker_consumer_loop_timeout()

    def process_item(self, item):
        if self.callable:
            return self.callable(item)
        else:
            raise ImproperlyConfiguredError("Provide callable or override 'process_item' method")

    def iteration(self):
        try:
            item = self.inbound_queue.get(timeout=self.timeout)
        except Empty:
            return

        self.process_item(item)
