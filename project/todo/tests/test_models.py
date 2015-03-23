from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.test import TestCase, RequestFactory
from todo.models import UserProfile, Task
from todo.models.request_log import RequestLogManager, RequestLog

from .utils import Utils


class FakeError(Exception):
    pass


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = Utils.create_test_user()

    def test_task_saving_invokes_task_count_incrementation(self):
        """
        Saving new task to the database should increment added_tasks_count variable on owner's user profile
        """
        Utils.create_task(self.user, 'Test content')

        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.added_tasks_count, 1, "Added tasks count don't match")

    def test_task_updating_doesn_not_invoke_task_count_incrementation(self):
        """
        Updating existing task does not increment added_tasks_count on user profile
        """
        task = Utils.create_task(self.user, 'Test content')
        task.content = "Changed content"
        task.save()

        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.added_tasks_count, 1, "Added tasks count don't match")


class UserTests(TestCase):
    def test_user_post_save_creates_user_profile(self):
        """
        Tests whether the creation of a new user invokes the creation of it's user profile.
        """
        user = Utils.create_test_user()
        user_profile = user.user_profile

        self.assertIsNotNone(user_profile)


class TestRequestLogManager(TestCase):
    fake_ip = '192.168.0.1'
    fake_method = 'get='
    fake_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
    fake_host = 'www.google.pl'
    fake_query_string = 'search=Django'

    def setUp(self):
        self.fake_request = self._create_fake_request()
        self.fake_response = self._create_fake_response()
        self.fake_exception = FakeError()

    def test_request_log_manager_creates_request_log_when_called_with_exception(self):
        """
        Test checks whether RequestLogManager returns RequestLog instance when called with exception and request
        """
        manager = RequestLogManager()
        request_log = manager.create_from_exception(request=self.fake_request, exception=self.fake_exception)

        self.assertIsInstance(request_log, RequestLog)

    def test_request_log_manager_saves_request_log_when_called_with_exception(self):
        """
        Test checks whether RequestLogManager is able to save RequestLog object in a database.
        """
        manager = RequestLogManager()
        request_log = manager.create_from_exception(request=self.fake_request, exception=self.fake_exception)

        self.assertIsNotNone(request_log.id)


    def test_request_log_manager_parses_request_and_exception(self):
        """
        Test checks whether RequestLogManager is able parse request and exception
        """
        manager = RequestLogManager()

        request_log = manager.create_from_exception(request=self.fake_request, exception=self.fake_exception)

        self.assertEquals(request_log.id, 1)
        self.assertEquals(request_log.ip, self.fake_ip)
        self.assertEquals(request_log.http_method, self.fake_method)
        self.assertEquals(request_log.user_agent, self.fake_user_agent)
        self.assertEquals(request_log.url, ("{}://{}?{}".format('http', self.fake_host, self.fake_query_string)))

    def test_request_log_manager_creates_request_log_when_called_with_response(self):
        """
        Test checks whether RequestLogManager returns RequestLog instance when called with response and request
        """
        manager = RequestLogManager()
        request_log = manager.create_from_response(request=self.fake_request, response=self.fake_response)

        self.assertIsInstance(request_log, RequestLog)

    def test_request_log_manager_saves_request_log_when_called_with_response(self):
        """
        Test checks whether RequestLogManager is able to save RequestLog object in a database.
        """
        manager = RequestLogManager()
        request_log = manager.create_from_response(request=self.fake_request, response=self.fake_response)

        self.assertIsNotNone(request_log.id)


    def test_request_log_manager_parses_request_and_response(self):
        """
        Test checks whether RequestLogManager is able parse request and response
        """
        manager = RequestLogManager()

        request_log = manager.create_from_response(request=self.fake_request, response=self.fake_response)

        self.assertEquals(request_log.id, 1)
        self.assertEquals(request_log.ip, self.fake_ip)
        self.assertEquals(request_log.http_method, self.fake_method)
        self.assertEquals(request_log.user_agent, self.fake_user_agent)
        self.assertEquals(request_log.url, ("{}://{}?{}".format('http', self.fake_host, self.fake_query_string)))

    def _create_fake_request(self):
        fake_request = HttpRequest()

        fake_request.META['CONTENT_LENGTH'] = '100'
        fake_request.META['REQUEST_METHOD'] = self.fake_method
        fake_request.META['REMOTE_ADDR'] = self.fake_ip
        fake_request.META['HTTP_X_FORWARDED_FOR'] = self.fake_ip
        fake_request.META['HTTP_USER_AGENT'] = self.fake_user_agent
        fake_request.META['HTTP_HOST'] = self.fake_host
        fake_request.META['QUERY_STRING'] = self.fake_query_string

        return fake_request

    def _create_fake_response(self):
        fake_response = HttpResponse()

        return fake_response
