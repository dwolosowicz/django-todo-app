from todo.models import Task


def task_count_processor(request):
    if request.user.is_authenticated():
        count = Task.objects.filter(user=request.user, is_completed=False).count()
    else:
        count = 0

    return {
        'task_count': count
    }
