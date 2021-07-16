from app.utils.response import JSONResponse


class HttpError(Exception):
    """Http Error Exception to be extended for various Http error status codes

    Attributes:
        errors: errors dictionary (optional) revealing more details to be sent in response
        response: response body to be sent
    """

    def __init__(self, status_code, message='', error_code=None, errors={}):
        response = {
            'statusCode': status_code,
            'error': {
                'message': message
            }
        }
        if error_code is not None:
            response['error']['code'] = error_code

        if errors is not None:
            response['error']['errors'] = errors

        setattr(self, 'errors', errors)
        setattr(self, 'response', JSONResponse(response, status=status_code))

        super(HttpError, self).__init__(self, message)


class BadRequest(HttpError):
    """Exception for HTTP 400 extended from HttpError

    The server cannot or will not process the request due to an apparent client error.
    """

    status_code = 400

    def __init__(self, message='The request is invalid. Please try again.',
                 error_code=None, errors=None):
        super(
            BadRequest,
            self).__init__(
            self.status_code,
            message,
            error_code,
            errors)


class Unauthorized(HttpError):
    """Exception for HTTP 401 extended from HttpError

    Use when authentication is required and has failed or has not yet been provided.
    Basically when access to resource needs login
    """

    status_code = 401

    def __init__(self, message='Sent request is unauthorized. Please log in first.',
                 error_code=None, errors=None):
        super(
            Unauthorized,
            self).__init__(
            self.status_code,
            message,
            error_code,
            errors)


class Forbidden(HttpError):
    """Exception for HTTP 403 extended from HttpError

    The user might be logged in but does not have the necessary permissions for the resource.
    """

    status_code = 403

    def __init__(
            self, message='You don\'t have necessary permissions to access this resource.', error_code=None, errors=None
    ):
        super(
            Forbidden,
            self).__init__(
            self.status_code,
            message,
            error_code,
            errors)


class NotFound(HttpError):
    """Exception for HTTP 404 extended from HttpError

    The requested resource could not be found but may be available in future.
    """

    status_code = 404

    def __init__(self, message='The resource you are looking for does not exist.',
                 error_code=None, errors=None):
        super(
            NotFound,
            self).__init__(
            self.status_code,
            message,
            error_code,
            errors)


class MethodNotAllowed(HttpError):
    """Exception for HTTP 405 extended from HttpError

    A request method is not supported for the requested resource.
    """

    status_code = 405

    def __init__(self, message='This method is not allowed for the sent request.',
                 error_code=None, errors=None):
        super(
            MethodNotAllowed,
            self).__init__(
            self.status_code,
            message,
            error_code,
            errors)


class InternalServerError(HttpError):
    """Exception for HTTP 500 extended from HttpError

    A generic error message, error_code=None, given when an unexpected condition was encountered and no more specific
    message is suitable.
    """

    status_code = 500

    def __init__(
            self,
            message='Looks like something went wrong! Please try again.\nIf the issue persists please contact support.',
            error_code=None, errors=None
    ):
        super(
            InternalServerError,
            self).__init__(
            self.status_code,
            message,
            error_code,
            errors)
