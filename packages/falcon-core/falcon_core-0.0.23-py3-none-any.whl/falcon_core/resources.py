import json

from falcon import HTTPNotFound


def dict_from_req(req):
    if req.content_length:
        try:
            return json.load(req.stream)
        except json.JSONDecodeError:
            return {}
    return {}


class Resource:
    storage = {}

    def on_get(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_post(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_put(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_delete(self, req, resp, **kwargs):
        raise HTTPNotFound


class JSONResourceBase(type):
    def __new__(mcs, name, bases, attrs):
        http_methods = ('get', 'post', 'put', 'delete')
        http_handlers = {}

        for obj_name, obj in attrs.items():
            if obj_name.startswith(http_methods) and 'on_' + obj_name not in attrs.keys():
                http_handlers['on_' + obj_name] = lambda i, req, resp, **kw: obj(i, req, resp, dict_from_req(req), **kw)

        attrs.update(http_handlers)

        return super().__new__(mcs, name, bases, attrs)


class JSONResource(metaclass=JSONResourceBase):
    storage = {}

    def get(self, req, resp, data, **kwargs):
        raise HTTPNotFound

    def post(self, req, resp, data, **kwargs):
        raise HTTPNotFound

    def put(self, req, resp, data, **kwargs):
        raise HTTPNotFound

    def delete(self, req, resp, data, **kwargs):
        raise HTTPNotFound
