BASE_DIR = None

SECRET_KEY = ''

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'falcon_core',
]

DEFAULT_MEDIA_TYPE = 'falcon.MEDIA_JSON'

REQUEST_TYPE = 'falcon.request.Request'

RESPONSE_TYPE = 'falcon.response.Response'

MIDDLEWARE = []

ROUTER = 'falcon.routing.DefaultRouter'

INDEPENDENT_MIDDLEWARE = False

ROUTER_CONVERTERS = {}

ROUTES = ''

WSGI_APPLICATION = ''

DEPLOY = {}
