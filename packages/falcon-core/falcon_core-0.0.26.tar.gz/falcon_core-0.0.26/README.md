# falcon Core
Falcon Core Inspired by Django for Falcon API Framework.
## Installation
```bash
pip install falcon-core
```
## User guide
### Starting project
```bash
falcon-core startproject api
```
Create project api and folder api 
- api/
- api/manage.py
- apy/api/
- apy/api/\_\_init\_\_.py
- apy/api/settings.py
- apy/api/routes.py
- apy/api/wsgi.py
```bash
falcon-core startproject api .
```
Create project api in my location folder
- my_location/manage.py
- my_location/api/
- my_location/api/\_\_init\_\_.py
- my_location/api/settings.py
- my_location/api/routes.py
- my_location/api/wsgi.py
```bash
falcon-core startproject api folder
```
Create project api in folder
- folder/manage.py
- folder/api/
- folder/api/\_\_init\_\_.py
- folder/api/settings.py
- folder/api/routes.py
- folder/api/wsgi.py
### Starting project app
```bash
python manage.py startapp example
```
Create app in project dir
- example/\_\_init\_\_.py
- example/resources.py
- example/routes.py
```bash
python manage.py startapp example.example1
```
Create app in app
- example/example1/\_\_init\_\_.py
- example/example1/resources.py
- example/example1/routes.py
```bash
python manage.py startapp example2.example3
```
- example2/\_\_init\_\_.py
- example2/example3/\_\_init\_\_.py
- example2/example3/resources.py
- example2/example3/routes.py
### Create resource in example.resource.py
```text
import falcon

from falcon_core.resources import Resource


class ExampleResource(Resource):
    def on_get(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_OK
        resp.media = {'key': 'value'}

```
### Add resource to routes
example.routes.py
```text
from falcon_core.routes import route

from example.resources import ExampleResource

routes = [
    route('/example', ExampleResource()),
]
```
(1) api.resource.py
```text
from falcon_core.routes import route, include

from example.routes import routes as example_routes

routes = [
    route('', include(example_routes)),
]
```
(2) api.routes.py
```text
from falcon_core.routes import route, include

routes = [
    route('', include('example.routes')),
]
```
### Add middleware
In api.settings.py
```text
...
MIDDLEWARE = [
    'module.MiddlewareOrMiddlewareInstance'
]
...
```
### Add router converters
In api.settings.py
```text
...
ROUTER_CONVERTERS = [
    'name': 'module.Converter'
]
...
```
### Change root routes
In api.settings.py
```text
...
ROUTES = 'module.routes'  # must have routes list
...
```
