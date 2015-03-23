from todo.models import UserProfile, Task
from django.contrib.auth.models import User


class Utils:

    @classmethod
    def create_task(cls, user, content, priority=Task.NORMAL):
        return Task.objects.create(
            user=user,
            content=content,
            priority=priority)

    @classmethod
    def create_test_user(cls, username='test_user', email='test_email@gmail.com', password='test_pass'):
        return User.objects.create_user(username, email, password)
