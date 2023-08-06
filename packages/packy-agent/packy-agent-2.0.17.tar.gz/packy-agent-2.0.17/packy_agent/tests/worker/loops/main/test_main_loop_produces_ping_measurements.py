import json

import httpretty
import gevent
import pytest
from sqlalchemy import create_engine

from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.models.sqlalchemy.base import Session
from packy_agent.domain_logic.models.sqlalchemy.measurement import Measurement
from packy_agent.tests.worker.loops.main.base import start_main_loop, stop_main_loop


TASKS = [
    {
        'module_name': 'ping', 'args': [], 'id': 1,
        'kwargs': {
            'number_of_pings': 3,
            'host': '8.8.8.8',
            'interval_ms': 0,
            'packet_size': 64
        },
        'schedule': '*/2 * * * * *'
    },
]


@pytest.mark.usefixtures('activated')
def test_main_loop_produces_ping_measurements():
    main_loop = start_main_loop(TASKS)
    gevent.sleep(2)

    engine = create_engine(settings.get_database_url())
    with Session(engine) as session:
        measurements = session.query(Measurement).all()

    assert measurements
    for measurement in measurements:
        assert measurement.id
        assert measurement.measurement_type == 1
        assert measurement.created_at_ts
        assert not measurement.submitted_at_ts

        value_dict = json.loads(measurement.value)
        assert isinstance(value_dict['ts'], int)
        assert value_dict['target'] == '8.8.8.8'
        assert value_dict['n_pings'] == 3
        assert value_dict['packet_size'] == 64
        assert isinstance(value_dict['values'], list)
        if value_dict['values']:
            assert isinstance(value_dict['values'][0], (float, int))

    for task in main_loop.tasks:
        task.stop()

    gevent.sleep(2)

    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/agent/module/ping/measurement/'
        httpretty.register_uri(httpretty.POST, url, status=201)

        gevent.sleep(3)

        latest_requests = httpretty.HTTPretty.latest_requests
        assert latest_requests
        measurements_submitted = 0
        for request in latest_requests:
            if request.path == '/api/v2/agent/module/ping/measurement/':
                body = json.loads(request.body)
                assert isinstance(body['ts'], int)
                assert body['target'] == '8.8.8.8'
                assert body['n_pings'] == 3
                assert body['packet_size'] == 64
                assert isinstance(body['values'], list)
                if body['values']:
                    assert all(isinstance(value, (float, int)) for value in body['values'])

                measurements_submitted += 1

        assert measurements_submitted > 0

    with Session(engine) as session:
        not_submitted = session.query(Measurement).filter_by(submitted_at_ts=None).all()
        assert not not_submitted

    stop_main_loop(main_loop)
