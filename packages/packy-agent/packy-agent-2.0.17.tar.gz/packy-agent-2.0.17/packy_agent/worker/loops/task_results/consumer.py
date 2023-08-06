from packy_agent.worker.loops.base.consumer import ConsumerLoop
from packy_agent.constants import CONSUMER_LOOP
from packy_agent.clients.local_storage import get_local_storage


class TaskResultsConsumer(ConsumerLoop):

    formal_name = CONSUMER_LOOP

    def __init__(self, inbound_queue=None, timeout=None):
        super().__init__(inbound_queue, timeout=timeout)

        self.collected_counter = 0

    def process_item(self, item):
        get_local_storage().save_measurement(item)
        self.collected_counter += 1
