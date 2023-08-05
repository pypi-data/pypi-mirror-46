import os
import importlib

from falcon_core.config import global_settings

ENVIRONMENT_VARIABLE = 'FALCON_CORE_SETTINGS_MODULE'


class LazySettings:
    _wrapped = None

    def __getattr__(self, item):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, item)

    def _setup(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise EnvironmentError(f'Set environment variable {ENVIRONMENT_VARIABLE}.')
        self._wrapped = Settings(settings_module)

    def __repr__(self):
        if self._wrapped is None:
            return '<LazySettings [Unevaluated]>'
        return f'<LazySettings "{self._wrapped.SETTINGS_MODULE}">'


class Settings:
    def __init__(self, settings_module):
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        self.SETTINGS_MODULE = settings_module
        module = importlib.import_module(self.SETTINGS_MODULE)

        tuple_settings = (
            'INSTALLED_APPS',
        )

        self._explicit_settings = set()

        for setting in dir(module):
            if setting.isupper():
                setting_value = getattr(module, setting)

                if setting in tuple_settings and not isinstance(setting_value, (list, tuple)):
                    raise TypeError(f'{setting} must be a list or a tuple.')
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

        if not self.SECRET_KEY:
            raise AttributeError('The SECRET_KEY setting must not be empty.')

    def __repr__(self):
        return f'<{type(self).__name__} {self.SETTINGS_MODULE}>'


settings = LazySettings()
