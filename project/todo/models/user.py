from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

