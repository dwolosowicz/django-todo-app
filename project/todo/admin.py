from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from todo.models import Task, RequestLog

admin.site.unregister(User)


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_display = ('type', 'ip', 'url', 'http_method', 'body_length')
    list_display_links = None

    def type(self, instance):
        if instance.exception_name is None:
            return "{} - {}".format("Status", instance.status_code)
        else:
            return "{} - {}".format("Exception", instance.exception_name)

    type.short_description = "Result"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('is_completed', 'content', 'priority', 'created', 'modified', 'user')
    list_filter = ('user', 'priority', 'created', 'modified')
    search_fields = ('content',)
    ordering = ('created', 'modified')

@admin.register(User)
class TodoUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'added_tasks_count')

    def added_tasks_count(self, instance):
        return instance.user_profile.added_tasks_count

    added_tasks_count.short_description = 'Tasks added'
