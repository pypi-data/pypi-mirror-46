from importlib import import_module

from falcon import API

from falcon_core.config import settings

from falcon_core.utils import import_object, load_middleware, flatten


def get_wsgi_application():
    media_type = import_object(settings.DEFAULT_MEDIA_TYPE)
    request_type = import_object(settings.REQUEST_TYPE)
    response_type = import_object(settings.RESPONSE_TYPE)
    middleware = [load_middleware(m) for m in settings.MIDDLEWARE]
    router = import_object(settings.ROUTER)
    independent_middleware = settings.INDEPENDENT_MIDDLEWARE

    application = API(media_type=media_type, request_type=request_type, response_type=response_type,
                      middleware=middleware, router=router(), independent_middleware=independent_middleware)

    for k, v in settings.ROUTER_CONVERTERS.items():
        application.router_options.converters[k] = import_object(v)

    for route in flatten(import_module(settings.ROUTES).routes):
        application.add_route(route.uri_template, route.resource, **route.kwargs)

    return application
