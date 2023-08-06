import tempfile

import pytest

from packy_agent.configuration.sources.base import YamlFileBackedSource


def test_yaml_file_backed_source():
    with tempfile.NamedTemporaryFile(buffering=0) as f:
        f.write(b'value1: 10\nvalue2: 15')

        source = YamlFileBackedSource(f.name)
        assert set(source) == {'value1', 'value2'}
        assert source['value1'] == 10
        assert source['value2'] == 15
        assert 'value1' in source
        assert source.get('value1') == 10
        assert source.get('value3', 4) == 4
        assert sorted(source.keys()) == ['value1', 'value2']
        assert sorted(source.values()) == [10, 15]
        assert sorted(source.items()) == [('value1', 10), ('value2', 15)]

        with pytest.raises(TypeError) as ex:
            source['value1'] = 0

        assert "'YamlFileBackedSource' object does not support item assignment" in str(ex.value)

        with pytest.raises(TypeError) as ex:
            del source['value1']
        assert "'YamlFileBackedSource' object does not support item deletion" in str(ex.value)

        with pytest.raises(AttributeError) as ex:
            source.pop('value1')
        assert "'YamlFileBackedSource' object has no attribute 'pop'" in str(ex.value)
