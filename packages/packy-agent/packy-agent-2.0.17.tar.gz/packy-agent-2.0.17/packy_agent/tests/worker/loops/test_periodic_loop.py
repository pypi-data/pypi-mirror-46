import gevent

from packy_agent.worker.loops.base.periodic import PeriodicLoop


def test_periodic_loop_survives_exception_in_callable():
    counter = 0
    with_exception = False

    def call_me():
        nonlocal counter
        if with_exception:
            raise Exception('Test exception')
        counter += 1

    loop = PeriodicLoop(0.5, call_me)
    loop.start()
    gevent.sleep(1)
    with_exception = True
    counter_value_before_exception = counter
    assert counter_value_before_exception
    gevent.sleep(1)
    with_exception = False
    gevent.sleep(1)
    assert counter > counter_value_before_exception
    loop.stop()
    gevent.sleep(1)
