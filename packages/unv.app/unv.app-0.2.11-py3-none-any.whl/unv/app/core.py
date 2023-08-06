import os
import copy
import importlib

import cerberus

from unv.utils.collections import update_dict_recur


def convert_value(value):
    if value == 'False':
        value = False
    elif value == 'True':
        value = True
    elif value.isdigit():
        value = int(value)
    return value


class ComponentSettings:
    KEY = ''
    SCHEMA = {}
    DEFAULTS = {}

    @staticmethod
    def create(settings: dict = None, base_settings: dict = None) -> dict:
        """Create app settings, overrided by env."""
        settings = settings or {}
        if base_settings:
            settings = update_dict_recur(settings, base_settings)
        for key, value in os.environ.items():
            if 'SETTINGS_' not in key:
                continue
            current_settings = settings
            parts = [
                part.lower()
                for part in key.replace('SETTINGS_', '').split('_')
            ]
            last_index = len(parts) - 1
            for index, part in enumerate(parts):
                if index == last_index:
                    current_settings[part] = convert_value(value)
                else:
                    current_settings = current_settings.setdefault(part, {})
        return settings

    def __init__(self):
        key = self.__class__.KEY
        if not key:
            raise ValueError(f"Provide 'KEY' for settings")

        module_path = os.environ.get('SETTINGS', 'app.settings.development')
        module = importlib.import_module(module_path)

        app_settings = module.SETTINGS
        app_schema = getattr(module, 'SCHEMA', {})

        settings = copy.deepcopy(self.__class__.DEFAULTS)
        settings = update_dict_recur(
            settings, app_settings.get(self.__class__.KEY, {}))

        schema = app_schema.get(
            self.__class__.KEY, self.__class__.SCHEMA)

        validator = cerberus.Validator(schema)
        if not validator.validate(settings):
            raise ValueError(f"Error validation settings {validator.errors}")

        self._data = settings
        self._schema = schema
