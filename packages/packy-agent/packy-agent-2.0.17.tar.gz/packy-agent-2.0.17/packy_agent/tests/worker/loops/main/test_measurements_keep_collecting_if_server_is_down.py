import json

import pytest
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


def assert_stored_value(value):
    assert isinstance(value['ts'], int)
    assert value['target'] == '8.8.8.8'
    assert value['n_pings'] == 3
    assert value['packet_size'] == 64
    assert isinstance(value['values'], list)
    if value['values']:
        assert isinstance(value['values'][0], (float, int))


@pytest.mark.usefixtures('activated')
def test_measurements_keep_collecting_if_server_is_down():
    run_main_loop(TASKS)

    engine = create_engine(settings.get_database_url())
    with Session(engine) as session:
        measurements = session.query(Measurement).order_by(Measurement.created_at_ts).all()

    assert measurements
    for measurement in measurements:
        assert measurement.id
        assert measurement.measurement_type == 1
        assert measurement.created_at_ts
        assert not measurement.submitted_at_ts

        assert_stored_value(json.loads(measurement.value))

    first_measurement = measurements[0]
    assert first_measurement.error_at_ts
    assert first_measurement.error_message
    assert first_measurement.error_message.startswith('Could not connect to server:')
