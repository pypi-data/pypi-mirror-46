import os
import socket
import getpass
import platform
import subprocess

from falcon_core.management.base import BaseCommand
from falcon_core.config import settings


def get_gunicorn_config():
    return """[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User={user}
Group=www-data
WorkingDirectory={path}
ExecStart={gunicorn} --access-logfile - --workers 3 --bind unix:{sock} {name}.wsgi:application

[Install]
WantedBy=multi-user.target"""


def get_nginx_config():
    return """server {{
    listen 80;
    server_name {domains};

    location / {{
        include proxy_params;
        proxy_pass http://unix:{sock};
    }}

    {extras}
}}"""


def paths_exists(*args):
    if not args:
        raise ValueError('Not set arg or args.')
    for arg in args:
        if not os.path.exists(arg):
            return False
    return True


class DeployError(Exception):
    pass


class Command(BaseCommand):
    def _setup(self):
        self.hostname = socket.gethostname()
        self.path = os.getcwd()
        self.user = getpass.getuser()

        self.settings = getattr(settings, 'DEPLOY', {})

        self.gunicorn_config = self.settings.get('GUNICORN_CONFIG', get_gunicorn_config())

        self.nginx_config = self.settings.get('NGINX_CONFIG', get_nginx_config())

        self.nginx_extras = self.settings.get('NGINX_EXTRAS', '')

        self.app = {'path': settings.BASE_DIR, 'name': os.path.basename(settings.BASE_DIR)}

        self.gunicorn = {
            'name': 'gunicorn_{}.service'.format(self.app['name']),
            'file': os.path.join(self.app['name'], 'gunicorn_{}.service'.format(self.app['name'])),
            'enabled_dir': os.path.abspath(os.path.join(os.sep, 'etc', 'systemd', 'system')),
            'enabled_file': os.path.join(os.path.abspath(os.path.join(os.sep, 'etc', 'systemd', 'system')),
                                         'gunicorn_{}.service'.format(self.app['name'])),
            'sock': os.path.join(self.app['path'], '{}.sock'.format(self.app['name'])),
        }

        self.nginx = {
            'name': self.app['name'], 'file': os.path.join(self.app['name'], self.app['name']),
            'available_dir': os.path.abspath(os.path.join(os.sep, 'etc', 'nginx', 'sites-available')),
            'available_file': os.path.join(os.path.abspath(os.path.join(os.sep, 'etc', 'nginx', 'sites-available')),
                                           self.app['name']),
            'enabled_dir': os.path.abspath(os.path.join(os.sep, 'etc', 'nginx', 'sites-enabled')),
            'enabled_file': os.path.join(os.path.abspath(os.path.join(os.sep, 'etc', 'nginx', 'sites-enabled')),
                                         self.app['name'])
        }

        self.domains = ' '.join(settings.ALLOWED_HOSTS)

        if not self.domains or '*' in self.domains:
            raise ValueError('Set correct domains.')

    def add_arguments(self, parser):
        parser.add_argument('--restart', action='store_true', dest='restart', help='Restart gunicorn and nginx.')
        parser.add_argument('--stop', action='store_true', dest='stop', help='Stop gunicorn and nginx.')

    def handle(self, *args, **options):
        if platform.system() == 'Linux':
            self._setup()
            if options.get('restart') and not options.get('stop'):
                self.restart()
            elif not options.get('restart') and options.get('stop'):
                self.stop()
            elif not options.get('restart') and not options.get('stop'):
                self.deploy()
        else:
            print('Only for Linux OS!')

    def command_call(self, command):
        command = 'sudo {}'.format(command)
        print('{}@{}:{}# {}'.format(self.user, self.hostname, self.path, command))
        subprocess.call(command, shell=True)

    def deploy(self):
        self.stop()

        with open(self.gunicorn['file'], 'w') as gc:
            gunicorn_config = self.gunicorn_config.format(
                user=self.user, path=self.app['path'],
                gunicorn=os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'gunicorn'),
                sock=self.gunicorn['sock'], name=self.app['name'])
            print('{}\n'.format(gunicorn_config))
            gc.write(gunicorn_config)

        self.command_call('mv {} {}'.format(self.gunicorn['file'], self.gunicorn['enabled_dir']))
        self.command_call('systemctl daemon-reload')
        self.command_call('systemctl restart {}'.format(self.gunicorn['name']))
        self.command_call('systemctl start {}'.format(self.gunicorn['name']))
        self.command_call('systemctl enable {}'.format(self.gunicorn['name']))
        self.command_call('systemctl status {}'.format(self.gunicorn['name']))

        with open(self.nginx['file'], 'w') as nc:
            nginx_config = self.nginx_config.format(domains=self.domains, path=self.app['path'],
                                                    sock=self.gunicorn['sock'], extras=self.nginx_extras)
            print('{}\n'.format(nginx_config))
            nc.write(nginx_config)

        self.command_call('mv {} {}'.format(self.nginx['file'], self.nginx['available_dir']))
        self.command_call('ln -s {} {}'.format(self.nginx['available_file'], self.nginx['enabled_dir']))
        self.command_call('nginx -t')
        self.command_call('systemctl restart nginx')
        self.command_call('ufw allow \'Nginx Full\'')

    def restart(self):
        if paths_exists(self.gunicorn['enabled_file'], self.nginx['enabled_file']):
            self.command_call('systemctl daemon-reload')
            self.command_call('systemctl restart {}'.format(self.gunicorn['name']))
            self.command_call('systemctl restart nginx')
        else:
            raise DeployError()

    def stop(self):
        self.command_call('systemctl stop nginx')

        if paths_exists(self.gunicorn['enabled_file']):
            self.command_call('rm {}'.format(self.gunicorn['enabled_file']))

        if paths_exists(self.nginx['available_file']):
            self.command_call('rm {}'.format(self.nginx['available_file']))

        if paths_exists(self.nginx['enabled_file']):
            self.command_call('rm {}'.format(self.nginx['enabled_file']))

        if paths_exists(self.gunicorn['sock']):
            self.command_call('rm {}'.format(self.gunicorn['sock']))

        self.command_call('systemctl start nginx')
