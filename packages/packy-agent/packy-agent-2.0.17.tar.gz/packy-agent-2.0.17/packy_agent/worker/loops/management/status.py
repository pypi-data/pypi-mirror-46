import logging

import gevent
from gevent.pywsgi import WSGIServer
from gevent.greenlet import Greenlet
from flask import Flask
from flask import jsonify

from packy_agent.constants import STATUS_LOOP
from packy_agent.worker.loops.base.misc import StartableStoppableLoop
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.worker.loops.base.scheduled import ScheduledLoop


logger = logging.getLogger(__name__)


class StatusLoop(StartableStoppableLoop):

    formal_name = STATUS_LOOP

    def __init__(self, main_loop, address='127.0.0.1', port=5000, **mkwargs):
        mkwargs.pop('is_safe_iteration', None)
        mkwargs.pop('is_logged_iteration', None)
        super().__init__(is_safe_iteration=False, is_logged_iteration=False, **mkwargs)

        self.main_loop = main_loop
        self.address = address
        self.port = port

        self._http_server = None

    def get_app(self):
        app = Flask(__name__)

        @app.route('/status/')
        def status():
            main_loop = self.main_loop

            loops = {}
            for loop in main_loop.loops:
                loop_greenlet = loop.get_greenlet()
                is_greenlet_dead = loop_greenlet.dead if loop_greenlet else None

                loop_properties = {
                    'is_running': getattr(loop, 'is_running', None),
                    'is_greenlet_dead': is_greenlet_dead,
                    'loop_type': loop.loop_type,
                    'counter': loop.counter,
                }

                if isinstance(loop, PeriodicLoop):
                    loop_properties['period'] = loop.period

                if isinstance(loop, ScheduledLoop):
                    loop_properties['schedule'] = loop.schedule

                produced_counter = getattr(loop, 'produced_counter', None)
                if produced_counter is not None:
                    loop_properties['produced_counter'] = produced_counter

                loops[loop.formal_name] = loop_properties

            task_results_consumer = main_loop.task_results_consumer
            if task_results_consumer:
                collected_counter = task_results_consumer.collected_counter
            else:
                collected_counter = None

            task_results_submitter = main_loop.task_results_submitter
            if task_results_submitter:
                submitted_counter = task_results_submitter.submitted_counter
            else:
                submitted_counter = None

            task_results_purger = main_loop.task_results_purger
            if task_results_purger:
                purged_records = task_results_purger.purged_records
            else:
                purged_records = None

            payload = {
                'loops': loops,
                'collected_counter': collected_counter,
                'submitted_counter': submitted_counter,
                'purged_records': purged_records,
            }
            return jsonify(payload)

        return app

    def iteration(self):
        gevent.sleep(60)  # faking it

    def get_greenlet(self):
        return

    def start(self):
        logger.info('STARTED %s', self.description)
        self.is_running = False
        self.is_stopping = False

        if not self._http_server:
            self._http_server = WSGIServer((self.address, self.port), self.get_app())

        if not self._http_server.started:
            self._http_server.start()

    def join(self):
        try:
            self._http_server._stop_event.wait()
        finally:
            Greenlet.spawn(self.stop).join()

        logger.info('STOPPED %s', self.description)

    def stop(self):
        super().stop()
        if self._http_server:
            self._http_server.stop()
