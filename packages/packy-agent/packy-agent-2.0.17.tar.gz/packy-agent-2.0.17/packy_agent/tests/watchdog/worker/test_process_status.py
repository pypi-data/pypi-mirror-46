import os
from unittest.mock import MagicMock, patch

import pytest

from packy_agent.watchdog.service import WatchdogService


def get_pid_mock(target):
    if target == 'worker':
        return os.getpid()

    return 9999999999999999999999


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_process_is_running():
    with patch('packy_agent.watchdog.service.control_manager.get_pid', get_pid_mock) as get_pid:
        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock(return_value=None)
        service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
        service.resolve_worker_response = MagicMock(return_value=None)

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_process_is_not_running():
    with patch('packy_agent.watchdog.service.control_manager.get_pid') as get_pid:
        get_pid.return_value = 9999999999999999999999
        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock(return_value=None)
        service.resolve_worker_supervisor_program_status = MagicMock(return_value=None)
        service.resolve_worker_response = MagicMock(return_value=None)

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_called()
        service.reboot.assert_not_called()
