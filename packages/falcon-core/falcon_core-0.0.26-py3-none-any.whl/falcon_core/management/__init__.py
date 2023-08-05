import os
import sys
import pkgutil
from importlib import import_module

from falcon_core.config import ENVIRONMENT_VARIABLE, settings, global_settings


def find_commands(management_dir):
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg]


def load_command_class(app_name, name):
    module = import_module(f'{app_name}.management.commands.{name}')
    return module.Command()


def execute_command_from_argv(argv):
    if len(argv) > 1:
        command = argv[1]
        commands = {}
        if os.environ.get(ENVIRONMENT_VARIABLE):
            apps_names = settings.INSTALLED_APPS
        else:
            apps_names = global_settings.INSTALLED_APPS
        for app_name in apps_names:
            app = import_module(app_name)
            management_dir = os.path.join(os.path.dirname(app.__file__), 'management')
            if os.path.exists(management_dir):
                commands.update({name: load_command_class(app_name, name) for name in find_commands(management_dir)})
        commands[command].run_from_argv(argv)


def execute_from_command_line(argv=None):
    execute_command_from_argv(argv or sys.argv)
