from todo.models import RequestLog
from django.utils import timezone


class RequestLoggingMiddleware():
    def process_response(self, request, response):
        RequestLog.objects.create_from_response(request, response)

        return response

    def process_exception(self, request, exception):
        RequestLog.objects.create_from_exception(request, exception)


class TimezoneMiddleware():
    def process_request(self, request):
        tz = request.user.user_profile.timezone

        timezone.activate(tz);
