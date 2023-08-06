from unittest.mock import patch

import gevent
from sqlalchemy import create_engine

from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.models.sqlalchemy.base import Session
from packy_agent.domain_logic.models.sqlalchemy.measurement import Measurement
from packy_agent.tests.worker.loops.main.base import start_main_loop, stop_main_loop

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


def test_purger():
    main_loop = start_main_loop(TASKS)
    gevent.sleep(1)
    main_loop.task_results_consumer.stop()
    main_loop.task_results_submitter.stop()
    while main_loop.task_results_consumer.is_running or main_loop.task_results_submitter.is_running:
        gevent.sleep(1)

    gevent.sleep(5)  # Let get measurements
    engine = create_engine(settings.get_database_url())
    with Session(engine) as session:
        measurements = session.query(Measurement).order_by(Measurement.created_at_ts).all()

    assert measurements

    with patch('packy_agent.worker.loops.task_results.purger.get_available_disk_space',
               new=lambda path=None: 0):
        gevent.sleep(2)

    with Session(engine) as session:
        measurements = session.query(Measurement).order_by(Measurement.created_at_ts).all()

    assert not measurements

    stop_main_loop(main_loop)
