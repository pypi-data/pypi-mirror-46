import logging
import json

from sanic.handlers import ErrorHandler
from xintian.exception import CustomException

logger = logging.getLogger('xintian')


def jsonify(records):
    """
    Parse database record response into JSON format
    """
    return [dict(r.items()) for r in records]


class CustomHandler(ErrorHandler):

    def default(self, request, exception):
        if isinstance(exception, CustomException):
            data = {
                'message': exception.message,
                'code': exception.code,
            }
            if exception.error:
                data.update({'error': exception.error})
            return json.dumps(data, status=exception.status_code)
        return super().default(request, exception)
