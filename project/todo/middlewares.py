from todo.models import RequestLog


class RequestLoggingMiddleware(object):
    def process_response(self, request, response):
        RequestLog.objects.create_from_response(request, response)

        return response

    def process_exception(self, request, exception):
        RequestLog.objects.create_from_exception(request, exception)