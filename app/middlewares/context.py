import threading
import uuid

from django.urls import resolve

ctx = threading.local()


def get_current_context():
    """
    :return: Current Request Context
    """
    return ctx


class ContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ctx.request = request

        trace_id = str(uuid.uuid4())
        setattr(request, 'trace_id', trace_id)
        request_parameters = resolve(request.path_info)
        request.url_info = {
            'kwargs': request_parameters.kwargs,
            'url_name': request_parameters.url_name,
            'app_names': request_parameters.app_names,
            'app_name': request_parameters.app_name,
            'namespaces': request_parameters.namespaces,
            'namespace': request_parameters.namespace,
            'view_name': request_parameters.view_name
        }
        response = self.get_response(request)
        del ctx.request
        return response
