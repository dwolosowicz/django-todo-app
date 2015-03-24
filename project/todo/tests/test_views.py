from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from urlparse import urlparse
from django.core import mail
from django.contrib.auth.models import User

from .utils import Utils
from todo.models import RequestLog


class AuthAsserts(TestCase):

    def assertLoggedIn(self, client, user):
        self.assertEqual(client.session['_auth_user_id'], user.pk)


class HttpAsserts(TestCase):

    def assertSuccess(self, response):
        self.assertEqual(200, response.status_code)

    def assertRedirect301(self, response):
        self.assertEqual(301, response.status_code)

    def assertRedirect302(self, response):
        self.assertEqual(302, response.status_code)

    def assertBadRequest(self, response):
        self.assertEqual(400, response.status_code)

    def assertNotFound(self, response):
        self.assertEqual(404, response.status_code)


class TaskTest(HttpAsserts, TestCase):

    class TestUser:
        def __init__(self):
            self.instance = Utils.create_test_user(username=self.username, password=self.password, email=self.email);


    class TestUserOne(TestUser):
        username = 'user_a'
        password = 'password_user_a'
        email = 'user_a@user.com'


    class TestUserTwo(TestUser):
        username = 'user_b'
        password = 'password_user_b'
        email = 'user_b@user.com'


    def test_annonymous_create_task(self):
        """
        Tests whether not logged user can access and create a new task.
        """

        c = Client()
        response = c.post(reverse('task_new'))

        url_components = urlparse(response.url)

        self.assertRedirect302(response)
        self.assertEquals(reverse('login')[:-1], url_components.path)

    def test_task_cross_modification(self):
        """
        Tests whether an user A can modify the task of an user B
        """

        c = Client()

        user_a = self.TestUserOne()
        user_b = self.TestUserTwo()

        user_a_task = Utils.create_task(user_a.instance, "My custom content")

        login_status = c.login(username=user_b.username, password=user_b.password)

        response = c.post(
            reverse('task_content'), {
                'content': 'Changed content', 'id': user_a_task.id})

        self.assertTrue(login_status)
        self.assertNotFound(response)


class RequestLogTest(TestCase):

    def test_request_log_logs_requests_correctly(self):
       c = Client()

       response = c.post(reverse('login')) # Request will create request log internally

       login_request_log = RequestLog.objects.get(pk=1)
       self.assertEqual(login_request_log.ip, "127.0.0.1")
       self.assertEqual(login_request_log.body_length, response.request['CONTENT_LENGTH'])
       self.assertEqual(login_request_log.user_agent, '')

       self.assertEqual(login_request_log.status_code, response.status_code)


class AuthTest(AuthAsserts, HttpAsserts, TestCase):

    def test_user_can_login(self):
        user = Utils.create_test_user(
            'user',
            'user@example.com',
            'test_pass')

        c = Client()
        response = c.post(reverse('login'), { 'username': 'user', 'password': 'test_pass' })

        self.assertRedirect302(response)
        self.assertLoggedIn(c, user)

    def test_user_can_register_and_mail_is_sent(self):
        c = Client()

        response = c.post(reverse('register'), {
                'username': 'Test',
                'password': 'test_pass',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'test@example.com',
                'timezone': 'Europe/Warsaw'
            })

        self.assertRedirect302(response)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(User.objects.get(pk=1))
