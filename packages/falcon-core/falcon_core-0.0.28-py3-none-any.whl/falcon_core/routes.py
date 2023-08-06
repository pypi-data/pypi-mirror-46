from importlib import import_module

from falcon_core.utils import flatten


class Route:
    def __init__(self, uri_template, resource, **kwargs):
        if not uri_template or uri_template.startswith('/') and '//' not in uri_template:
            self.uri_template = uri_template
            self.resource = resource
            self.kwargs = kwargs
        else:
            raise ValueError(f'Route uri_template \'{uri_template}\' is not valid.')


def route(*args, **kwargs):
    ri = Route(*args, **kwargs)
    if isinstance(ri.resource, list):
        ri.resource = flatten(ri.resource)
        for r in ri.resource:
            r.uri_template = f'{ri.uri_template}{r.uri_template}'
        return ri.resource
    return ri


def include(routes):
    if isinstance(routes, str):
        return import_module(routes).routes
    return routes
