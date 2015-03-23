from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from urlparse import urlparse

from .utils import Utils
from todo.models import RequestLog


class TaskTest(TestCase):

    def test_annonymous_create_task(self):
        """
        Tests whether not logged user can access and create a new task.
        """

        c = Client()
        response = c.post(reverse('task_new'))

        url_components = urlparse(response.url)

        self.assertEquals(302, response.status_code)
        self.assertEquals(reverse('login')[:-1], url_components.path)

    def test_task_cross_modification(self):
        """
        Tests whether an user A can modify the task of an user B
        """

        c = Client()

        user_b_username = 'user_b'
        user_b_password = 'test_pass'

        user_a = Utils.create_test_user(
            'user_a',
            'user_a@example.com',
            'test_pass')
        user_b = Utils.create_test_user(
            user_b_username,
            'user_b@example.com',
            user_b_password)

        user_a_task = Utils.create_task(user_a, "My custom content")

        login_status = c.login(username=user_b_username, password=user_b_password)

        response = c.post(
            reverse('task_content'), {
                'content': 'Changed content', 'id': user_a_task.id})

        self.assertTrue(login_status)
        self.assertEquals(400, response.status_code)


class RequestLogTest(TestCase):

    def test_request_log_logs_requests_correctly(self):
       c = Client()

       response = c.post(reverse('login')) # Request will create request log internally

       login_request_log = RequestLog.objects.get(pk=1)
       self.assertEqual(login_request_log.ip, "127.0.0.1")
       self.assertEqual(login_request_log.body_length, response.request['CONTENT_LENGTH'])
       self.assertEqual(login_request_log.user_agent, '')

       self.assertEqual(login_request_log.status_code, response.status_code)


class LoginTest(TestCase):

    def test_user_can_login(self):
        user = Utils.create_test_user(
            'user',
            'user@example.com',
            'test_pass')

        c = Client()
        response = c.post(reverse('login'), { 'username': 'user', 'password': 'test_pass' })

        self.assertEquals(302, response.status_code) # Check whether the client passed through the form
        self.assertEqual(c.session['_auth_user_id'], user.pk) # Determine if is truly logged in
