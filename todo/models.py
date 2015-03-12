from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields


class Task(models.Model):
    LOW = 'L'
    NORMAL = 'N'
    HIGH = 'H'

    PRIORITIES = (
        ('', 'Choose the priority'),
        (LOW, 'Low'),
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
    )

    user = models.ForeignKey(User)
    content = models.TextField(default='')
    priority = models.CharField(max_length=1, choices=PRIORITIES)
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    content.short_description = 'Name'

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, related_name='user_profile')
    timezone = models.CharField(max_length=128, null=None).null
    added_tasks_count = models.IntegerField(default=0)

    def increment_tasks_count(self):
        self.added_tasks_count += 1

    def __str__(self):
        return str(self.user)


# Create corresponding UserProfile right after user creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)


# Increment user profiles added_task_count variable
@receiver(post_save, sender=Task)
def increment_tasks_added(sender, instance, **kwargs):
    if kwargs.get('created') is False:
        return

    profile = instance.user.user_profile
    profile.increment_tasks_count()
    profile.save()

