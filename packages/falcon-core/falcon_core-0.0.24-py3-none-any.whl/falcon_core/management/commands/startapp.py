import os

from falcon_core.management.base import BaseCommand
from falcon_core.management.utils import create_package, create_module
from falcon_core.config import settings


def startapp(app_name, app_path):
    create_module(app_path, 'resources', 'from falcon_core.resources import Resource\n')
    create_module(app_path, 'routes', 'from falcon_core.routes import route\n\nroutes = []\n')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('app_name', action='store')

    def handle(self, *args, **kwargs):
        app_name = kwargs.pop('app_name')
        if '.' in app_name:
            app_name = app_name.split('.')
            app_path = settings.BASE_DIR
            for name in app_name:
                app_path = os.path.join(app_path, name)
                create_package(app_path)
            app_name = app_name[-1]
            startapp(app_name, app_path)
        else:
            app_path = os.path.join(settings.BASE_DIR, app_name)
            create_package(app_path)
            startapp(app_name, app_path)
