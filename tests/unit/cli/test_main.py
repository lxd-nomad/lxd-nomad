import os
import unittest.mock

import pytest

from lxdock.cli.main import LXDock, main
from lxdock.cli.project import get_project
from lxdock.conf.config import Config
from lxdock.conf.exceptions import ConfigError
from lxdock.container import Container
from lxdock.exceptions import LXDockException
from lxdock.project import Project


FIXTURE_ROOT = os.path.join(os.path.dirname(__file__), 'fixtures')


@unittest.mock.patch.object(LXDock, 'help')
def test_main_function_can_run_a_lxdock_command(mock_help_action):
    main(['help'])
    assert mock_help_action.call_count == 1


class TestLXDock:
    @unittest.mock.patch.object(LXDock, 'project_config')
    @unittest.mock.patch.object(Config, 'serialize')
    def test_can_display_the_config_file_of_the_project(self, serialize_mock, mock_config):
        mock_config.__get__ = unittest.mock.Mock(
            return_value=Config.from_base_dir(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['config'])
        assert serialize_mock.call_count == 1

    @unittest.mock.patch.object(LXDock, 'project_config')
    @unittest.mock.patch.object(Config, 'serialize')
    def test_can_display_the_containers_of_the_config_file_of_the_project(
            self, serialize_mock, mock_config):
        mock_config.__get__ = unittest.mock.Mock(
            return_value=Config.from_base_dir(os.path.join(FIXTURE_ROOT, 'project01')))
        argv = ['config', '--containers']
        n = LXDock(argv)
        assert serialize_mock.call_count == 0
        assert n._parsers['main'].parse_args(argv).containers

    @unittest.mock.patch('builtins.input', return_value='Y')
    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'destroy')
    @unittest.mock.patch.object(Container, 'exists')
    def test_can_run_the_destroy_action_for_all_containers_of_a_project(
            self, container_exists_mock, mock_project_destroy, mock_project, y_mock):
        container_exists_mock.__get__ = unittest.mock.Mock(return_value=True)
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['destroy'])
        assert mock_project_destroy.call_count == 1
        assert mock_project_destroy.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch('builtins.input', return_value='Y')
    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'destroy')
    @unittest.mock.patch.object(Container, 'exists')
    def test_can_run_the_destroy_action_for_specific_containers(
            self, container_exists_mock, mock_project_destroy, mock_project, y_mock):
        container_exists_mock.__get__ = unittest.mock.Mock(return_value=True)
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['destroy', 'default'])
        assert mock_project_destroy.call_count == 1
        assert mock_project_destroy.call_args == [{'container_names': ['default', ], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'destroy')
    @unittest.mock.patch.object(Container, 'exists')
    def test_can_run_the_destroy_containers_using_a_force_option(
            self, container_exists_mock, mock_project_destroy, mock_project):
        container_exists_mock.__get__ = unittest.mock.Mock(return_value=True)
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['destroy', '--force'])
        assert mock_project_destroy.call_count == 1
        assert mock_project_destroy.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'destroy')
    @unittest.mock.patch.object(Container, 'exists')
    def test_can_force_the_destroy_action_if_the_containers_do_not_exist(
            self, container_exists_mock, mock_project_destroy, mock_project):
        container_exists_mock.__get__ = unittest.mock.Mock(return_value=False)
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['destroy'])
        assert mock_project_destroy.call_count == 1
        assert mock_project_destroy.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'halt')
    def test_can_run_the_halt_action_for_all_containers_of_a_project(
            self, mock_project_halt, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['halt'])
        assert mock_project_halt.call_count == 1
        assert mock_project_halt.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'halt')
    def test_can_run_the_halt_action_for_specific_containers(
            self, mock_project_halt, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['halt', 'c1', 'c2'])
        assert mock_project_halt.call_count == 1
        assert mock_project_halt.call_args == [{'container_names': ['c1', 'c2', ], }, ]

    def test_can_print_the_global_help(self):
        argv = ['help']
        n = LXDock(argv)
        assert n._parsers['main'].parse_args(argv).subcommand is None

    def test_can_print_the_help_for_a_specific_subcommand(self):
        argv = ['help', 'up']
        n = LXDock(argv)
        assert n._parsers['main'].parse_args(argv).subcommand == 'up'

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'provision')
    def test_can_run_the_provision_action_for_all_containers_of_a_project(
            self, mock_project_provision, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['provision'])
        assert mock_project_provision.call_count == 1
        assert mock_project_provision.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'provision')
    def test_can_run_the_provision_action_for_specific_containers(
            self, mock_project_provision, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['provision', 'c1', 'c2'])
        assert mock_project_provision.call_count == 1
        assert mock_project_provision.call_args == [{'container_names': ['c1', 'c2', ], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'shell')
    def test_can_run_the_shell_action_for_all_containers_of_a_project(
            self, mock_project_shell, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['shell'])
        assert mock_project_shell.call_count == 1
        assert mock_project_shell.call_args == [{'container_name': None, 'username': None}, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'shell')
    def test_can_run_the_shell_action_for_a_specific_container(
            self, mock_project_shell, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['shell', 'c1'])
        assert mock_project_shell.call_count == 1
        assert mock_project_shell.call_args == [{'container_name': 'c1', 'username': None}, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'shell')
    def test_can_run_the_shell_action_for_a_specific_user(self, mock_project_shell, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['shell', '-u', 'foobar'])
        assert mock_project_shell.call_count == 1
        assert mock_project_shell.call_args == [{'container_name': None, 'username': 'foobar'}, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'status')
    def test_can_run_the_status_action_for_all_containers_of_a_project(
            self, mock_project_status, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['status'])
        assert mock_project_status.call_count == 1
        assert mock_project_status.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'status')
    def test_can_run_the_status_action_for_specific_containers(
            self, mock_project_status, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['status', 'c1', 'c2'])
        assert mock_project_status.call_count == 1
        assert mock_project_status.call_args == [{'container_names': ['c1', 'c2', ], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'up')
    def test_can_run_the_up_action_for_all_containers_of_a_project(
            self, mock_project_up, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['up'])
        assert mock_project_up.call_count == 1
        assert mock_project_up.call_args == [{'container_names': [], }, ]

    @unittest.mock.patch.object(LXDock, 'project')
    @unittest.mock.patch.object(Project, 'up')
    def test_can_run_the_up_action_for_specific_containers(
            self, mock_project_up, mock_project):
        mock_project.__get__ = unittest.mock.Mock(
            return_value=get_project(os.path.join(FIXTURE_ROOT, 'project01')))
        LXDock(['up', 'c1', 'c2'])
        assert mock_project_up.call_count == 1
        assert mock_project_up.call_args == [{'container_names': ['c1', 'c2', ], }, ]

    def test_exit_if_no_action_is_provided(self):
        with pytest.raises(SystemExit):
            LXDock([])

    def test_exit_if_a_cli_error_is_encountered(self):
        with pytest.raises(SystemExit):
            LXDock(['help', 'unknown'])

    @unittest.mock.patch.object(LXDock, 'project')
    def test_exit_if_a_config_error_is_encountered(self, mock_project):
        mock_project.__get__ = unittest.mock.Mock(side_effect=ConfigError(msg='TEST'))
        with pytest.raises(SystemExit):
            LXDock(['up'])

    @unittest.mock.patch.object(LXDock, 'project')
    def test_exit_if_a_lxdock_error_is_encountered(self, mock_project):
        mock_project.__get__ = unittest.mock.Mock(side_effect=LXDockException(msg='TEST'))
        with pytest.raises(SystemExit):
            LXDock(['up'])

    @unittest.mock.patch.object(Config, 'from_base_dir')
    def test_project_config_property_works(
            self, from_base_dir_mock):
        n = LXDock(['config'])
        config1, config2 = n.project_config, n.project_config
        assert config1 == config2
        assert from_base_dir_mock.call_count == 1

    @unittest.mock.patch.object(Config, 'from_base_dir')
    @unittest.mock.patch.object(Project, 'from_config')
    def test_project_property_works(
            self, from_config_mock, from_base_dir_mock):
        n = LXDock(['config'])
        project1, project2 = n.project, n.project
        assert project1 == project2
        assert from_config_mock.call_count == 1
