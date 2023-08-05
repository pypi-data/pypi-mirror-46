from waitress import serve

from falcon_core.wsgi import get_wsgi_application
from falcon_core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('address', action='store', nargs='?', default='127.0.0.1:8000')

    def handle(self, *args, **kwargs):
        address = kwargs.pop('address')
        host, port = address.split(':')
        serve(get_wsgi_application(), host=host, port=port)
