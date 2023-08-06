from packy_agent.configuration.sources.base import MappingBackedSource
from packy_agent.exceptions import ImproperlyConfiguredError
from packy_agent.configuration.sources.defaults_dict import defaults


def raise_improperly_configured_error(message):
    raise ImproperlyConfiguredError(message)


class ConfigurationDefaults(MappingBackedSource):

    def __init__(self, name=None):
        super().__init__(defaults, name=name or 'Defaults')
