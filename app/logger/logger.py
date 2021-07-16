import logging
import json

from app.middlewares.context import get_current_context


class ContextFilter(logging.Filter):
    """
    Add Context Info for every log record can be done here
    """

    def filter(self, record):
        # Stringifying objects
        if isinstance(record.msg, dict) or isinstance(record.msg, list):
            record.msg = json.dumps(record.msg)

        # Setting Trace id
        ctx = get_current_context()
        record.trace_id = ''
        request = getattr(ctx, 'request', None)
        if request:
            record.trace_id = request.trace_id
        return True


class CustomFormatter(logging.Formatter):
    def formatException(self, ei):
        res = super(CustomFormatter, self).formatException(ei)
        return json.dumps(res)


class Logger:
    log_format_string = 'PID-%(process)d> %(asctime)s:%(name)s:[%(module)s:%(funcName)20s():%(lineno)d]:' \
                        '%(levelname)s %(trace_id)s :: %(message)s'

    def __init__(self, logger_name, log_level=logging.DEBUG):
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        format_ = CustomFormatter(self.log_format_string)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(format_)
        logger.addHandler(console_handler)
        logger.addFilter(ContextFilter())
        logger.propagate = False
        self.logger = logger

    def get(self):
        return self.logger
