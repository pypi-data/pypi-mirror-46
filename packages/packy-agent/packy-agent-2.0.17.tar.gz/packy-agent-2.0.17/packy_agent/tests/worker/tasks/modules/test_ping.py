import time
from unittest.mock import MagicMock

import pytest
from gevent.queue import Queue

from packy_agent.worker.loops.modules.ping import ping, PingTaskLoop
from packy_agent.domain_logic.models.schematics.ping import PingModuleMeasurement
from packy_agent.exceptions import ImproperlyConfiguredError


def test_ping_smoke():
    measurement = ping(target='8.8.8.8')
    assert isinstance(measurement, PingModuleMeasurement)


def test_ping_smoke_host():
    measurement = ping(host='8.8.8.8')
    assert isinstance(measurement, PingModuleMeasurement)


def test_ping():
    measurement = ping(target='8.8.8.8')
    assert isinstance(measurement, PingModuleMeasurement)
    assert measurement.target == '8.8.8.8'
    assert measurement.packet_size == 64
    assert measurement.n_pings == 10
    assert isinstance(measurement.values_, list)
    assert measurement.values_
    for value in measurement.values_:
        assert isinstance(value, float)


def test_ping_domain_name():
    measurement = ping(target='google.com')
    assert isinstance(measurement, PingModuleMeasurement)
    assert measurement.target == 'google.com'
    assert measurement.packet_size == 64
    assert measurement.n_pings == 10
    assert isinstance(measurement.values_, list)
    assert measurement.values_
    for value in measurement.values_:
        assert isinstance(value, float)


def test_ping_unresolvable_target():
    measurement = ping(target='blahblahblah')
    assert isinstance(measurement, PingModuleMeasurement)
    assert isinstance(measurement.values_, list)
    assert not measurement.values_


def test_ping_with_interval():
    measurement = ping(target='8.8.8.8', interval_ms=50)
    assert isinstance(measurement, PingModuleMeasurement)
    assert measurement.target == '8.8.8.8'
    assert measurement.packet_size == 64
    assert measurement.n_pings == 10
    assert isinstance(measurement.values_, list)
    assert measurement.values_
    for value in measurement.values_:
        assert isinstance(value, float)


def test_ping_no_target_provided():
    assert ping() is None


def test_ping_task_loop_puts_to_queue():
    queue = Queue()
    loop = PingTaskLoop('*/1 * * * * *', kwargs={'target': '8.8.8.8'}, outbound_queue=queue)
    loop.croniter = MagicMock()
    loop.croniter.get_next.return_value = time.time() + 0.1
    loop.iteration_wrapper()

    assert len(queue) == 1
    measurement = queue.get()
    assert isinstance(measurement, PingModuleMeasurement)
    assert measurement.target == '8.8.8.8'
    assert measurement.packet_size == 64
    assert measurement.n_pings == 10
    assert isinstance(measurement.values_, list)
    assert measurement.values_
    for value in measurement.values_:
        assert isinstance(value, float)
