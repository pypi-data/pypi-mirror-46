import json

import pytest
import httpretty
from sqlalchemy import create_engine

from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.models.sqlalchemy.base import Session
from packy_agent.domain_logic.models.sqlalchemy.measurement import Measurement
from packy_agent.tests.worker.loops.main.base import run_main_loop


TASKS = [
    {
        'id': 1,
        'module_name': 'ping',
        'args': [],
        'kwargs': {
            'number_of_pings': 3,
            'host': '8.8.8.8',
            'interval_ms': 0,
            'packet_size': 64
        },
        'schedule': '*/2 * * * * *'
    },
]
HTTP_STATUSES = (400, 401, 403, 404, 405, 406, 408, 429)


def assert_stored_value(value):
    assert isinstance(value['ts'], int)
    assert value['target'] == '8.8.8.8'
    assert value['n_pings'] == 3
    assert value['packet_size'] == 64
    assert isinstance(value['values'], list)
    if value['values']:
        assert isinstance(value['values'][0], (float, int))


@pytest.mark.slow
@pytest.mark.usefixtures('activated')
@pytest.mark.parametrize('http_status', HTTP_STATUSES)
def test_reported_to_sentry_if_server_returns_http4xx(http_status, sentry_server_mock):
    events = sentry_server_mock
    events.clear()

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/agent/module/ping/measurement/'
        httpretty.register_uri(httpretty.POST, url, status=http_status)
        run_main_loop(TASKS, stop_timeout=5)

    assert events
    first_event = events[0]
    assert first_event[
        'logentry']['message'].startswith(f'Server responded with HTTP{http_status}:')


@pytest.mark.slow
@pytest.mark.usefixtures('activated')
@pytest.mark.parametrize('http_status', HTTP_STATUSES)
def test_give_up_if_server_returns_http4xx(http_status):
    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/agent/module/ping/measurement/'
        httpretty.register_uri(httpretty.POST, url, status=http_status)
        run_main_loop(TASKS, stop_timeout=5)

    engine = create_engine(settings.get_database_url())
    with Session(engine) as session:
        measurements = session.query(Measurement).order_by(Measurement.created_at_ts).all()

    assert measurements
    measurements_iter = iter(measurements)
    first_measurement = next(measurements_iter)

    assert first_measurement.id
    assert first_measurement.measurement_type == 1
    assert first_measurement.created_at_ts
    assert first_measurement.error_at_ts
    assert first_measurement.error_message
    assert first_measurement.error_message.startswith(f'HTTP{http_status}:')
    assert not first_measurement.submitted_at_ts

    for measurement in measurements_iter:
        assert measurement.id
        assert measurement.measurement_type == 1
        assert measurement.created_at_ts
        assert not measurement.error_at_ts
        assert not measurement.error_message
        assert not measurement.submitted_at_ts

        assert_stored_value(json.loads(measurement.value))
