from waitress import serve

from falcon_core.management.base import BaseCommand
from falcon_core.config import settings
from falcon_core.utils import import_object


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('address', action='store', nargs='?', default='127.0.0.1:8000')

    def handle(self, *args, **kwargs):
        address = kwargs.pop('address')
        host, port = address.split(':')
        serve(import_object(settings.WSGI_APPLICATION), host=host, port=port)
