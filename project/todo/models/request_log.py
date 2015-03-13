from django.db import models


class RequestLogManager(models.Manager):
    def create_from_exception(self, request, exception):
        data = dict(self.__parse_request(request), **self.__parse_exception(exception))

        request_log = RequestLog(**data)
        request_log.save()

        return request_log

    def create_from_response(self, request, response):
        data = dict(self.__parse_request(request), **self.__parse_response(response))

        request_log = RequestLog(**data)
        request_log.save()

        return request_log

    @staticmethod
    def __parse_request(request):
        return {
            'ip': request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR'),
            'body_length': request.META.get('CONTENT_LENGTH') or 0,
            'http_method': request.META.get('REQUEST_METHOD').lower(),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'url': request.build_absolute_uri()
        }

    @staticmethod
    def __parse_response(response):
        return {
            'status_code': response.status_code
        }

    @staticmethod
    def __parse_exception(exception):
        return {
            'exception_name': exception.__class__.__name__
        }


class RequestLog(models.Model):
    objects = RequestLogManager()

    ip = models.IPAddressField()
    user_agent = models.TextField()
    http_method = models.CharField(max_length=10)
    body_length = models.IntegerField()
    url = models.TextField()
    status_code = models.IntegerField(null=True)
    exception_name = models.TextField(null=True)