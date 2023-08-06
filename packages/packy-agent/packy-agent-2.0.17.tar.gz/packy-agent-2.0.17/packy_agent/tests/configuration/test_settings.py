import os
import tempfile

from packy_agent.configuration.settings import Settings
from packy_agent.configuration.sources.base import MappingBackedSource


def test_settings_from_file():
    with tempfile.NamedTemporaryFile(buffering=0) as f:
        f.write(b'value1: 10\nvalue2: 15')

        os.environ['PACKY_AGENT_SETTINGS_FILENAME'] = f.name

        settings = Settings()

        assert settings.get_value1() == 10
        assert settings.get_value2() == 15


def test_settings_from_command_line():
    settings = Settings()
    settings.set_commandline_arguments({'value1': 10, 'value2': 15})

    assert settings.get_value1() == 10
    assert settings.get_value2() == 15


def test_runtime_settings():
    settings = Settings()
    assert settings.get_component() is None

    settings.set_runtime('component', 'test')

    assert settings.get_component() == 'test'


def test_nested_dicts():
    settings = Settings()

    settings._sources = (
        (MappingBackedSource(
            {
                '1': {'1.2': {
                        '1.2.2': 'new 122',  # replace value
                        '1.2.3': 'new 123',  # add new
                    }
                },
                '2': {'2.1': 'different type'},  # replace with different type
                '3': 'new 3',  # add new at root level
            }, name='priority 1'
        )),
        (MappingBackedSource(
            {
                '1': {
                    '1.1': {'1.1.1': '111'},
                    '1.2': {
                        '1.2.1': '121',
                        '1.2.2': '122',
                    }
                },
                '2': {
                    '2.1': {'2.1.1': '211'},
                    '2.2': {
                        '2.2.1': '221',
                        '2.2.2': '222',
                    }
                }
            }, name='priority 2'
        )),
    )

    value1 = settings.get_1()
    assert value1['1.2']['1.2.1'] == '121'
    assert value1['1.2']['1.2.2'] == 'new 122'
    assert value1['1.2']['1.2.3'] == 'new 123'

    value2 = settings.get_2()
    assert value2['2.1'] == 'different type'
    assert value2['2.2'] == {'2.2.1': '221', '2.2.2': '222'}

    value3 = settings.get_3()
    assert value3 == 'new 3'


def test_get_set_section():
    from packy_agent.configuration.settings import settings
    assert settings.get_console_test_key() is None
    settings.set_console_test_key('test_value')
    assert settings.get_console_test_key() == 'test_value'
    console = settings.get_console()
    assert 'test_key' in console
    assert console['test_key'] == 'test_value'
