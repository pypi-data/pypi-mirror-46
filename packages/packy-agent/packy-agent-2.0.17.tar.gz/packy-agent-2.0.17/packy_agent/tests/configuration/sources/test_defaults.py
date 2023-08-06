from packy_agent.configuration.sources.defaults import ConfigurationDefaults


def test_defaults_smoke():
    defaults = ConfigurationDefaults()
    assert 'log_level' in defaults
    assert defaults['log_level'] == 'WARNING'
