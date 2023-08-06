def test_save_a_key(key_value_storage_source):
    key_value_storage_source['test_key'] = 'test_value'
    assert key_value_storage_source['test_key'] == 'test_value'
