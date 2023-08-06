from unittest.mock import patch, call

from packy_agent.domain_logic.managers.control import control_manager


def test_start():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as mock:
        mock.side_effect = ('nginx RUNNING pid 11, uptime 1 minute', None)
        control_manager.start('worker')
        mock.assert_has_calls((call('start', ('worker',)),))


def test_start_nginx():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as sup_mock:
        with patch('packy_agent.domain_logic.managers.control.nginx_service') as nginx_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'is_inside_docker_container') as is_inside_docker_container_mock:
                is_inside_docker_container_mock.return_value = False
                nginx_mock.is_running.return_value = False
                control_manager.start('nginx')
                nginx_mock.start.assert_called()
                sup_mock.assert_not_called()


def test_start_nginx_in_docker():
    with patch('packy_agent.domain_logic.managers.control.run_supervisor_command') as sup_mock:
        with patch('packy_agent.domain_logic.managers.control.nginx_service') as nginx_mock:
            with patch('packy_agent.domain_logic.managers.control.'
                       'is_inside_docker_container') as is_inside_docker_container_mock:
                sup_mock.side_effect = ('nginx STOPPED', None)
                is_inside_docker_container_mock.return_value = True
                nginx_mock.is_running.return_value = False
                control_manager.start('nginx')
                sup_mock.assert_has_calls((call('start', ('nginx',)),), any_order=True)
