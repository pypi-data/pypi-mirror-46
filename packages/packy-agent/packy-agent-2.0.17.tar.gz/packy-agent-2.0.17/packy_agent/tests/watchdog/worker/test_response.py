from unittest.mock import MagicMock

import httpretty
import pytest

from packy_agent.watchdog.service import WatchdogService
from packy_agent.configuration.settings import settings
from packy_agent.tests.fixtures.configuration import override_settings


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_smoke():
    with httpretty.enabled():
        url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                            settings.get_worker_http_port())
        httpretty.register_uri(httpretty.GET, url, status=200, body='{"loops": {"loop1": {}}}')
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_loops_activity = MagicMock()
        service.resolve_workflow = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_not_responding():
    service = WatchdogService()

    service.reboot = MagicMock()
    service.restart_worker = MagicMock()
    service.start_worker = MagicMock()

    service.resolve_online_status = MagicMock(return_value=None)
    service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
    service.resolve_worker_process_status = MagicMock(return_value=None)
    service.resolve_loops_activity = MagicMock(return_value=None)
    service.resolve_workflow = MagicMock(return_value=None)

    service.loop_iteration()

    service.start_worker.assert_not_called()
    service.restart_worker.assert_called()
    service.reboot.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_http5xx_response():
    with httpretty.enabled():
        url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                            settings.get_worker_http_port())
        httpretty.register_uri(httpretty.GET, url, status=500)
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock(return_value=None)
        service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
        service.resolve_worker_process_status = MagicMock(return_value=None)
        service.resolve_loops_activity = MagicMock(return_value=None)
        service.resolve_workflow = MagicMock(return_value=None)
        service.report_error = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()

        service.report_error.assert_called()
        call_args = service.report_error.call_args
        assert call_args
        assert call_args[0]
        assert call_args[0][0].startswith('Packy Agent Worker returned HTTP500:')


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_no_loops_in_response():
    with httpretty.enabled():
        url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                            settings.get_worker_http_port())
        httpretty.register_uri(httpretty.GET, url, status=200, body='{}')
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock(return_value=None)
        service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
        service.resolve_worker_process_status = MagicMock(return_value=None)
        service.resolve_loops_activity = MagicMock(return_value=None)
        service.resolve_workflow = MagicMock(return_value=None)
        service.report_error = MagicMock()
        service.report_warning = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()
        service.resolve_loops_activity.assert_not_called()

        service.report_warning.assert_called()
        call_args = service.report_warning.call_args
        assert call_args
        assert call_args[0]
        assert call_args[0][0].startswith('Worker did not return running loops')


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_took_too_long():
    with override_settings(
            {'worker': {'expected_http_response_time_seconds': 0}}):
        with httpretty.enabled():
            url = 'http://{}:{}/status/'.format(settings.get_worker_http_bind_address(),
                                                settings.get_worker_http_port())
            httpretty.register_uri(httpretty.GET, url, status=200, body='{}')
            httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                                   status=200)  # emulate console running

            service = WatchdogService()

            service.reboot = MagicMock()
            service.restart_worker = MagicMock()
            service.start_worker = MagicMock()

            service.resolve_online_status = MagicMock(return_value=None)
            service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
            service.resolve_worker_process_status = MagicMock(return_value=None)
            service.resolve_loops_activity = MagicMock(return_value=None)
            service.resolve_workflow = MagicMock(return_value=None)
            service.report_error = MagicMock()
            service.report_warning = MagicMock()

            service.loop_iteration()

            service.start_worker.assert_not_called()
            service.restart_worker.assert_not_called()
            service.reboot.assert_not_called()
            service.resolve_loops_activity.assert_not_called()

            service.report_warning.assert_called()
            assert service.report_warning.call_args_list
            assert any(args[0][0].startswith('It took ') for args
                       in service.report_warning.call_args_list)
