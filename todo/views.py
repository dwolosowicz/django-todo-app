from django.shortcuts import render, get_object_or_404
from django.views import generic

from todo.models import Task

class IndexView(generic.ListView):
    template_name = "todo/index.html"

    def get_queryset(self):
        Task.objects.filter(user=self.request.user).order('-created_at')