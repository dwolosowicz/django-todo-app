from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Task
from .forms import TaskContentForm, TaskCompletedForm, TaskPriorityForm


class IndexView(generic.ListView):
    template_name = "todo/index.html"
    queryset = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, is_completed=False).order_by('-created')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def task():
    pass


def task_update_field(request, form, key):
    task = get_object_or_404(Task, pk=request.POST['id'])

    if form.is_valid():
        setattr(task, key, form.cleaned_data[key])
        task.save()

        return HttpResponse()
    else:
        return HttpResponse(status=400)


def task_content(request):
    return task_update_field(request, TaskContentForm(request.POST), 'content')


def task_priority(request):
    return task_update_field(request, TaskPriorityForm(request.POST), 'priority')


def task_completed(request):
    return task_update_field(request, TaskCompletedForm(request.POST), 'is_completed')
