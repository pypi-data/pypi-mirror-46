import importlib

from .core import ComponentSettings


class AppSettings(ComponentSettings):
    KEY = 'app'
    SCHEMA = {
        'env': {
            'type': 'string',
            'allowed': ['production', 'development', 'testing'],
            'required': True
        },
        'components': {
            'type': 'list',
            'empty': True,
            'schema': {'type': 'string'},
            'required': True
        }
    }
    DEFAULTS = {
        'env': 'development',
        'components': [],
    }

    @property
    def is_development(self):
        return self._data['env'] == 'development'

    @property
    def is_production(self):
        return self._data['env'] == 'production'

    @property
    def is_testing(self):
        return self._data['env'] == 'testing'

    def get_components(self):
        for component in self._data['components']:
            component = '{}.app'.format(component)
            yield importlib.import_module(component)


SETTINGS = AppSettings()
