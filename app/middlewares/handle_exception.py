from django.conf import settings
from django.http.response import (
    HttpResponse,
    JsonResponse,
    StreamingHttpResponse,
    HttpResponseNotAllowed
)
from api_auth.utils.http_error import (
    HttpError,
    InternalServerError,
    MethodNotAllowed
)
# from sentry_sdk import capture_exception

from api_auth.logger import Logger

logger = Logger(logger_name=__name__, log_level=10).get()


class HandleException:
    """Middleware for handling exceptions.

    Attributes:
        get_response: handler method of next middleware or view
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # overriding Django's inbuilt error handling
        setattr(settings, 'DEBUG_PROPAGATE_EXCEPTIONS', True)

    def __call__(self, request):
        """Handler method for middleware

        Args:
            request: Django's request object.

        Returns:
            Response passed by next middleware or view.

        """

        try:
            response = self.get_response(request)

            if isinstance(response, HttpResponseNotAllowed):
                raise MethodNotAllowed

            if isinstance(response, (HttpResponse, StreamingHttpResponse)):
                return response
            else:
                return JsonResponse(response)

        except HttpError as e:
            logger.error(e)
            return e.response

        except Exception as e:
            # # log unhandled exception
            # capture_exception(e)
            # # error_logger.error(log)
            # traceback.print_exc()
            logger.error(e, exc_info=True)

            # send default error response hiding sensitive exception details
            return InternalServerError().response
