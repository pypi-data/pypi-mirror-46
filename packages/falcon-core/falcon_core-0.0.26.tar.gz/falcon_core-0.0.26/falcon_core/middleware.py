from falcon_core.resources import dict_from_req


class JSONMiddleware:
    def process_request(self, req, resp):
        req.context['data'] = dict_from_req(req)
