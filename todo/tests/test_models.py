from django.contrib.auth.models import User
from django.test import TestCase
from todo.models import UserProfile, Task


class Utils:
    @classmethod
    def create_task(cls, user, content, priority=Task.NORMAL):
        return Task.objects.create(user=user, content=content, priority=priority)

    @classmethod
    def create_test_user(cls):
        return User.objects.create_user('test_user', 'test_email@email.com', 'test_pass')


class UserTests(TestCase):
    def test_user_post_save_creates_user_profile(self):
        """
        Tests whether the creation of a new user invokes the creation of it's user profile.
        """
        user = Utils.create_test_user()
        user_profile = user.user_profile

        self.assertIsNotNone(user_profile)


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