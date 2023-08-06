from unittest.mock import patch

from packy_agent.domain_logic.managers.control import control_manager


def test_get_pid():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as mock:
        mock.return_value = 'worker RUNNING pid 11, uptime 1 minute'
        assert control_manager.get_pid('worker') == 11
        mock.assert_called()


def test_get_status():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as mock:
        mock.return_value = 'worker RUNNING pid 11, uptime 1 minute'
        assert control_manager.get_status('worker') == ('RUNNING', 11, '1 minute')
        mock.assert_called()


def test_get_nginx_status():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as sup_mock:
        with patch('packy_agent.domain_logic.managers.control.nginx_service') as nginx_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'is_inside_docker_container') as is_inside_docker_container_mock:
                sup_mock.return_value = 'nginx STOPPED'
                is_inside_docker_container_mock.return_value = False
                nginx_mock.is_running.return_value = True
                nginx_mock.get_pid.return_value = 12
                assert control_manager.get_status('nginx') == ('RUNNING', 12, None)
                sup_mock.assert_not_called()


def test_get_nginx_status_in_docker():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as sup_mock:
        with patch('packy_agent.domain_logic.managers.control.nginx_service') as nginx_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'is_inside_docker_container') as is_inside_docker_container_mock:
                sup_mock.return_value = 'nginx RUNNING pid 11, uptime 1 minute'
                is_inside_docker_container_mock.return_value = True
                nginx_mock.is_running.return_value = False
                nginx_mock.get_pid.return_value = None
                assert control_manager.get_status('nginx') == ('RUNNING', 11, '1 minute')
                sup_mock.assert_called()


def test_get_worker_status_line():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as mock:
        mock.return_value = 'worker RUNNING pid 11, uptime 1 minute'
        assert control_manager.get_worker_status_line() == 'RUNNING (uptime 1 minute)'
        mock.assert_called()


def test_is_running():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as mock:
        mock.return_value = 'worker RUNNING pid 11, uptime 1 minute'
        assert control_manager.is_running('worker')
        mock.assert_called()


def test_is_stopped():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as mock:
        mock.return_value = 'worker STOPPED pid 11, uptime 1 minute'
        assert control_manager.is_stopped('worker')
        mock.assert_called()
