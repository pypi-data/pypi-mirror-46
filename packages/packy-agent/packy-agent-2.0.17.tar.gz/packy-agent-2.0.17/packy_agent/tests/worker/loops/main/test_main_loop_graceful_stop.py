import gevent
from packy_agent.tests.worker.loops.main.base import start_main_loop, stop_main_loop


TASKS = [
    {
        'module_name': 'ping', 'args': [], 'id': 1,
        'kwargs': {
            'number_of_pings': 3,
            'override': False,
            'host': '8.8.8.8',
            'interval_ms': 0,
            'packet_size': 64
        },
        'schedule': '*/1 * * * * *'
    },
]


def test_main_loop_graceful_stop():
    main_loop = start_main_loop(TASKS)
    stop_main_loop(main_loop)
