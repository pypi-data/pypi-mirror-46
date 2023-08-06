import os
from datetime import datetime

from falcon_core.config import ENVIRONMENT_VARIABLE
from falcon_core.management.base import BaseCommand
from falcon_core.management.utils import create_package, create_module
from falcon_core.utils import encrypt_sha256


def startproject(name, base_dir):
    base_module_dir = os.path.join(base_dir, name)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    create_module(base_dir, 'manage', f"""import os\n
from falcon_core import management\n
os.environ.setdefault('{ENVIRONMENT_VARIABLE}', '{name}.settings')\n
if __name__ == '__main__':
    management.execute_from_command_line()
""")
    create_package(base_module_dir)
    create_module(base_module_dir, 'settings', f"""import os\n
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n
SECRET_KEY = '{encrypt_sha256(os.getlogin() + name + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'\n
DEBUG = True\n
ALLOWED_HOSTS = ['localhost']\n
INSTALLED_APPS = [
    'falcon_core',
]\n
DEFAULT_MEDIA_TYPE = 'falcon.MEDIA_JSON'\n
REQUEST_TYPE = 'falcon.request.Request'\n
RESPONSE_TYPE = 'falcon.response.Response'\n
MIDDLEWARE = []\n
ROUTER = 'falcon.routing.DefaultRouter'\n
INDEPENDENT_MIDDLEWARE = False\n
ROUTER_CONVERTERS = {{}}\n
ROUTES = '{name}.routes'\n
WSGI_APPLICATION = '{name}.wsgi.application'\n
DEPLOY = {{}}
""")
    create_module(base_module_dir, 'routes', """from falcon_core.routes import route\n
routes = [
]
""")
    create_module(base_module_dir, 'wsgi', f"""import os\n
from falcon_core.wsgi import get_wsgi_application\n
os.environ.setdefault('{ENVIRONMENT_VARIABLE}', '{name}.settings')\n
application = get_wsgi_application()
""")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', help='Project name.')
        parser.add_argument('folder', help='Project folder.', nargs='?')

    def handle(self, *args, **kwargs):
        name = kwargs.pop('name')
        folder = kwargs.pop('folder')

        current_folder = os.getcwd()

        if folder is None:
            base_dir = os.path.join(current_folder, name)
            startproject(name, base_dir)
        elif folder == '.':
            base_dir = current_folder
            startproject(name, base_dir)
        else:
            base_dir = os.path.join(current_folder, folder)
            startproject(name, base_dir)
