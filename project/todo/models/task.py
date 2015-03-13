from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
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
    finished = models.BooleanField(default=False)
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    content.short_description = 'Name'

    def __str__(self):
        return self.content

    @classmethod
    def priority_label(cls, key):
        for priorityTuple in cls.PRIORITIES:
            tuple_key, tuple_label = priorityTuple

            if key == tuple_key:
                return tuple_label.lower()

# Increment user profiles added_task_count variable
@receiver(post_save, sender=Task)
def increment_tasks_added(sender, instance, **kwargs):
    if kwargs.get('created') is True:
        profile = instance.user.user_profile
        profile.increment_tasks_count()
        profile.save()
