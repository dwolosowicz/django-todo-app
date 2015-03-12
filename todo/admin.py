from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from todo.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('content', 'priority', 'created', 'modified', 'user')

admin.site.unregister(User)
@admin.register(User)
class TodoUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'added_tasks_count')

    def added_tasks_count(self, instance):
        return instance.user_profile.added_tasks_count

    added_tasks_count.short_description = 'Tasks added'