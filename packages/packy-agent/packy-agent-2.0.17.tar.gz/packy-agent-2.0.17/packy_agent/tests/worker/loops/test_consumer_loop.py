import gevent
from gevent.queue import Queue

from packy_agent.worker.loops.base.consumer import ConsumerLoop


def test_scheduled_loop_survives_exception_in_callable():
    queue = Queue()
    counter = 0

    def call_me(item):
        nonlocal counter
        if not item:
            raise Exception('Test exception')
        counter += 1

    loop = ConsumerLoop(queue, call_me)
    loop.start()
    queue.put(1)
    gevent.sleep(1)
    counter_value_before_exception = counter
    assert counter_value_before_exception
    queue.put(None)
    gevent.sleep(1)
    queue.put(1)
    gevent.sleep(1)
    assert counter > counter_value_before_exception
    loop.stop()
    gevent.sleep(1)
