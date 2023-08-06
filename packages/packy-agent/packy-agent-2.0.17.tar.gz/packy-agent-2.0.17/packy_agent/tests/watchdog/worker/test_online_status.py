import time
from unittest.mock import MagicMock

import pytest
import httpretty

from packy_agent.configuration.settings import settings
from packy_agent.watchdog.service import WatchdogService
from packy_agent.tests.fixtures.configuration import override_settings


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_online_status_for_restart():
    with override_settings(
            {'worker': {'offline_to_restart_seconds': 10, 'restart_wait_seconds': 5}}):
        with httpretty.enabled():
            url = settings.get_server_base_url() + 'api/v2/agent/'
            httpretty.register_uri(httpretty.GET, url, status=200, body='{"is_online": false}')
            httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                                   status=200)  # emulate console running

            service = WatchdogService()
            service.last_known_online_ts = time.time() - 11

            service.reboot = MagicMock()
            service.restart_worker = MagicMock()
            service.resolve_worker_supervisor_program_status = MagicMock()
            service.resolve_worker_process_status = MagicMock()
            service.resolve_worker_response = MagicMock()

            service.loop_iteration()

            service.restart_worker.assert_called()
            service.reboot.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_online_status_for_reboot():
    now_ts = time.time()
    with override_settings(
            {'worker': {'offline_to_reboot_seconds': 10, 'reboot_wait_seconds': 5},
             'rebooted_at_ts': now_ts - 12}):
        with httpretty.enabled():
            url = settings.get_server_base_url() + 'api/v2/agent/'
            httpretty.register_uri(httpretty.GET, url, status=200, body='{"is_online": false}')
            httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                                   status=200)  # emulate console running

            service = WatchdogService()
            service.last_known_online_ts = time.time() - 11

            service.reboot = MagicMock()
            service.restart_worker = MagicMock()
            service.resolve_worker_supervisor_program_status = MagicMock()
            service.resolve_worker_process_status = MagicMock()
            service.resolve_worker_response = MagicMock()

            service.loop_iteration()

            service.reboot.assert_called()
            service.restart_worker.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_online_status_for_ok():
    with httpretty.enabled():
        url = settings.get_server_base_url() + 'api/v2/agent/'
        httpretty.register_uri(httpretty.GET, url, status=200, body='{"is_online": true}')
        httpretty.register_uri(httpretty.GET, settings.get_console_base_url(),
                               status=200)  # emulate console running

        service = WatchdogService()
        service.last_known_online_ts = time.time() - 11

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_worker_response = MagicMock()

        service.loop_iteration()

        service.reboot.assert_not_called()
        service.restart_worker.assert_not_called()
