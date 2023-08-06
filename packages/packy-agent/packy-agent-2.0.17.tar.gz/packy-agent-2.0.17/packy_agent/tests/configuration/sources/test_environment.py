import os

import pytest

from packy_agent.configuration.sources.environment import Environment


def test_environment_smoke():
    os.environ['PACKY_AGENT_SMOKE'] = 'smoke test'
    conf = Environment()
    assert 'smoke' in conf
    assert conf['smoke'] == 'smoke test'


def test_mapping_backed_source():
    for key in os.environ:
        if key.startswith('PACKY_AGENT_'):
            del os.environ[key]

    os.environ['PACKY_AGENT_STRING'] = 'test'
    os.environ['PACKY_AGENT_INT'] = '10'
    os.environ['PACKY_AGENT_FLOAT'] = '1.5'
    os.environ['PACKY_AGENT_BOOLEAN'] = 'true'

    source = Environment()
    assert set(source) == {'string', 'int', 'float', 'boolean'}
    assert source['string'] == 'test'
    assert source['int'] == 10
    assert source['float'] == 1.5
    assert source['boolean']
    assert 'string' in source
    assert source.get('string') == 'test'
    assert source.get('something', 4) == 4
    assert sorted(source.keys()) == sorted(('string', 'int', 'float', 'boolean'))
    source.values()  # smoke
    assert sorted(source.items()) == [('boolean', True), ('float', 1.5), ('int', 10),
                                      ('string', 'test')]

    with pytest.raises(TypeError) as ex:
        source['value1'] = 0

    assert "'Environment' object does not support item assignment" in str(ex.value)

    with pytest.raises(TypeError) as ex:
        del source['value1']
    assert "'Environment' object does not support item deletion" in str(ex.value)

    with pytest.raises(AttributeError) as ex:
        source.pop('value1')
    assert "'Environment' object has no attribute 'pop'" in str(ex.value)


def test_environment_getitem_coercion():
    os.environ['PACKY_AGENT_STRING'] = 'test'
    os.environ['PACKY_AGENT_INT'] = '10'
    os.environ['PACKY_AGENT_FLOAT'] = '1.5'
    os.environ['PACKY_AGENT_BOOLEAN'] = 'true'
    os.environ['PACKY_AGENT_DICT'] = '{2: 3}'
    conf = Environment()
    assert 'string' in conf
    assert conf['string'] == 'test'
    assert 'int' in conf
    assert conf['int'] == 10
    assert isinstance(conf['int'], int)
    assert 'float' in conf
    assert conf['float'] == 1.5
    assert 'boolean' in conf
    assert conf['boolean']
    assert isinstance(conf['boolean'], bool)
    assert 'dict' in conf
    assert conf['dict'] == {2: 3}
    assert isinstance(conf['dict'], dict)


def test_environment_supports_nestings():
    os.environ['PACKY_AGENT_CONSOLE_HTTP_PORT'] = '9000'
    os.environ['PACKY_AGENT_SUPERVISOR_A'] = '1'
    os.environ['PACKY_AGENT_WORKER_B'] = '2'
    os.environ['PACKY_AGENT_WATCHDOG_C'] = '3'
    conf = Environment()
    assert 'console' in conf
    assert conf['console'] == {'http_port': 9000}
    assert 'supervisor' in conf
    assert conf['supervisor'] == {'a': 1}
    assert 'worker' in conf
    assert conf['worker'] == {'b': 2}
    assert 'watchdog' in conf
    assert conf['watchdog'] == {'c': 3}
