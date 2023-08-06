from unittest.mock import MagicMock

import pytest

from packy_agent.watchdog.service import WatchdogService


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_loop_iteration():
    service = WatchdogService()
    service.loop_iteration()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_all_worker_resolves_tried():
    service = WatchdogService()
    service.resolve_online_status = MagicMock(return_value=None)
    service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
    service.resolve_worker_process_status = MagicMock(return_value=None)
    service.resolve_worker_response = MagicMock(return_value=None)
    service.loop_iteration()

    service.resolve_online_status.assert_called()
    service.resolve_worker_supervisor_program_status.assert_called()
    service.resolve_worker_process_status.assert_called()
    service.resolve_worker_response.assert_called()
