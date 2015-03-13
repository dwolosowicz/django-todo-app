from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from todo.models import Task


class IndexView(generic.ListView):
    template_name = "todo/index.html"
    queryset = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, finished=False).order_by('-created')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)