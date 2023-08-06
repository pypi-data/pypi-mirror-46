import time

from unittest.mock import patch, call, MagicMock

from packy_agent.tests.fixtures.configuration import override_settings
from packy_agent.domain_logic.managers.control import control_manager


def test_stop():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as run_mock:
        with patch('packy_agent.domain_logic.managers.control.Process') as process_cls_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'control_manager.terminate_process'):
                with patch('packy_agent.domain_logic.managers.control.'
                           'control_manager.kill_process'):
                    process_mock = MagicMock()
                    process_mock.is_running.return_value = False
                    process_cls_mock.return_value = process_mock

                    def side_effect(command, cargs, *args, **kwargs):
                        return (f'{cargs[0]} RUNNING pid 11, uptime 1 minute'
                                if command == 'status' else None)

                    run_mock.side_effect = side_effect
                    control_manager.stop('worker')
                    run_mock.assert_has_calls(
                        (call('stop', ('worker',), is_async=False,
                              async_delay_seconds=None, async_dev_null=False),), any_order=True)
                    control_manager.terminate_process.assert_not_called()
                    control_manager.kill_process.assert_not_called()


def test_terminate():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as run_mock:
        with patch('packy_agent.domain_logic.managers.control.Process') as process_cls_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'control_manager.terminate_process'):
                with patch('packy_agent.domain_logic.managers.control.'
                           'control_manager.kill_process'):
                    with override_settings({'process_stop_timeout_seconds': 0.2,
                                            'process_status_check_period_seconds': 0.02}):

                        terminate_at = time.time() + 0.5

                        def process_is_running_side_effect():
                            if time.time() >= terminate_at:
                                return False

                            return True

                        process_mock = MagicMock()
                        process_mock.is_running.side_effect = process_is_running_side_effect
                        process_cls_mock.return_value = process_mock

                        def side_effect(command, cargs, *args, **kwargs):
                            if command == 'status':
                                if time.time() >= terminate_at:
                                    return f'{cargs[0]} STOPPED'
                                else:
                                    return f'{cargs[0]} RUNNING pid 11, uptime 1 minute'

                        run_mock.side_effect = side_effect
                        control_manager.stop('worker')
                        run_mock.assert_has_calls(
                            (call('stop', ('worker',), is_async=False,
                                  async_delay_seconds=None, async_dev_null=False),), any_order=True)
                        control_manager.terminate_process.assert_called()
                        control_manager.kill_process.assert_not_called()


def test_kill():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as run_mock:
        with patch('packy_agent.domain_logic.managers.control.Process') as process_cls_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'control_manager.terminate_process'):
                with patch('packy_agent.domain_logic.managers.control.'
                           'control_manager.kill_process'):
                    with override_settings({'process_stop_timeout_seconds': 0.2,
                                            'sigterm_timeout_seconds': 0.2,
                                            'process_status_check_period_seconds': 0.02}):

                        terminate_at = time.time() + 0.5

                        def process_is_running_side_effect():
                            if time.time() >= terminate_at:
                                return False

                            return True

                        process_mock = MagicMock()
                        process_mock.is_running.side_effect = process_is_running_side_effect
                        process_cls_mock.return_value = process_mock

                        def side_effect(command, cargs, *args, **kwargs):
                            if command == 'status':
                                if time.time() >= terminate_at:
                                    return f'{cargs[0]} STOPPED'
                                else:
                                    return f'{cargs[0]} RUNNING pid 11, uptime 1 minute'

                        run_mock.side_effect = side_effect
                        control_manager.stop('worker')
                        run_mock.assert_has_calls(
                            (call('stop', ('worker',), is_async=False,
                                  async_delay_seconds=None, async_dev_null=False),), any_order=True)
                        control_manager.terminate_process.assert_called()
                        control_manager.kill_process.assert_called()
