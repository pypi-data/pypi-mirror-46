import json

from falcon import HTTPNotFound


class Resource:
    def on_get(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_post(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_put(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_delete(self, req, resp, **kwargs):
        raise HTTPNotFound


def dict_from_req(req):
    if req.content_length:
        try:
            return json.load(req.stream)
        except json.JSONDecodeError:
            return {}
    return {}


class JSONResourceBase(type):
    def __new__(mcs, name, bases, attrs):
        http_handlers = ('on_get', 'on_post', 'on_put', 'on_delete')

        for obj_name, obj in attrs.items():
            if obj_name.startswith(http_handlers):
                def http_handler(instance, req, resp, **kwargs):
                    req.context['data'] = dict_from_req(req)
                    obj(instance, req, resp, **kwargs)

                attrs[obj_name] = http_handler

        return super().__new__(mcs, name, bases, attrs)


class JSONResource(Resource, metaclass=JSONResourceBase):
    pass
