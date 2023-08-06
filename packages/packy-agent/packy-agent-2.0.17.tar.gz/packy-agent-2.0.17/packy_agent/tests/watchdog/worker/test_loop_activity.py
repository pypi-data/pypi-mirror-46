import time
import json
from unittest.mock import MagicMock
from copy import deepcopy

import httpretty
import pytest

from packy_agent.watchdog.service import WatchdogService
from packy_agent.configuration.settings import settings
from packy_agent.tests.fixtures.configuration import override_settings


loops = {
    'ping_module': {
        'counter': 1,
        'is_greenlet_dead': False,
        'is_running': True,
        'loop_type': 'scheduled_producer',
        'produced_counter': 1,
        'schedule': '*/1 * * * * *'
    }
}


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_smoke():
    with httpretty.enabled():
        url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                            settings.get_worker_http_port())
        httpretty.register_uri(httpretty.GET, url, status=200, body=json.dumps({'loops': loops}))
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_workflow = MagicMock()
        service.report_error = MagicMock()
        service.report_warning = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()

        service.report_warning.assert_not_called()
        service.report_error.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_smoke_2_iterations():
    with httpretty.enabled():
        url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                            settings.get_worker_http_port())
        httpretty.register_uri(httpretty.GET, url, status=200, body=json.dumps({'loops': loops}))
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_workflow = MagicMock()
        service.report_error = MagicMock()
        service.report_warning = MagicMock()

        service.loop_iteration()
        time.sleep(0.2)
        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()

        service.report_warning.assert_not_called()
        service.report_error.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_smoke_2_iterations_counter_change():
    with httpretty.enabled():
        url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                            settings.get_worker_http_port())
        httpretty.register_uri(httpretty.GET, url, status=200, body=json.dumps({'loops': loops}))
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_workflow = MagicMock()
        service.report_error = MagicMock()
        service.report_warning = MagicMock()

        service.loop_iteration()
        time.sleep(0.2)

        loops_copy = deepcopy(loops)
        loops_copy['ping_module']['counter'] = 2
        httpretty.register_uri(httpretty.GET, url, status=200,
                               body=json.dumps({'loops': loops_copy}))
        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()

        service.report_warning.assert_not_called()
        service.report_error.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_counter_stale():
    with override_settings({'watchdog': {'relax_period_seconds': 0}}):
        with httpretty.enabled():
            url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                                settings.get_worker_http_port())
            httpretty.register_uri(httpretty.GET, url, status=200, body=json.dumps({'loops': loops}))
            httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                                   status=200)  # emulate console running

            service = WatchdogService()

            service.reboot = MagicMock()
            service.restart_worker = MagicMock()
            service.start_worker = MagicMock()

            service.resolve_online_status = MagicMock(return_value=None)
            service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
            service.resolve_worker_process_status = MagicMock(return_value=None)
            service.resolve_workflow = MagicMock(return_value=None)
            service.report_error = MagicMock()
            service.report_warning = MagicMock()

            service.loop_iteration()
            assert 'ping_module' in service.loop_stats
            assert 'change_deadline_ts' in service.loop_stats['ping_module']
            assert service.loop_stats['ping_module']['change_deadline_ts'] is not None
            time.sleep(1.5)

            service.loop_iteration()

            service.start_worker.assert_not_called()
            service.restart_worker.assert_not_called()
            service.reboot.assert_not_called()

            service.report_error.assert_not_called()
            service.report_warning.assert_called()
            assert service.report_warning.call_args_list
            assert any('counter is stale on' in args[0][0] for args
                       in service.report_warning.call_args_list)


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_counter_not_stale():
    with override_settings({'watchdog': {'relax_period_seconds': 0}}):
        with httpretty.enabled():
            url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                                settings.get_worker_http_port())
            httpretty.register_uri(httpretty.GET, url, status=200,
                                   body=json.dumps({'loops': loops}))
            httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                                   status=200)  # emulate console running

            service = WatchdogService()

            service.reboot = MagicMock()
            service.restart_worker = MagicMock()
            service.start_worker = MagicMock()

            service.resolve_online_status = MagicMock(return_value=None)
            service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
            service.resolve_worker_process_status = MagicMock(return_value=None)
            service.resolve_workflow = MagicMock(return_value=None)
            service.report_error = MagicMock()
            service.report_warning = MagicMock()

            service.loop_iteration()
            assert 'ping_module' in service.loop_stats
            assert 'change_deadline_ts' in service.loop_stats['ping_module']
            assert service.loop_stats['ping_module']['change_deadline_ts'] is not None
            time.sleep(1.5)

            loops_copy = deepcopy(loops)
            loops_copy['ping_module']['counter'] = 2
            httpretty.register_uri(httpretty.GET, url, status=200,
                                   body=json.dumps({'loops': loops_copy}))
            service.loop_iteration()

            service.start_worker.assert_not_called()
            service.restart_worker.assert_not_called()
            service.reboot.assert_not_called()

            service.report_error.assert_not_called()
            service.report_warning.assert_not_called()
