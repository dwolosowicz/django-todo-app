from django.conf.urls import url, patterns
from todo import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^task$', views.task, name="task_new"),
    url(r'^task/content$', views.task_content, name="task_content"),
    url(r'^task/priority$', views.task_priority, name="task_priority"),
    url(r'^task/completed$', views.task_completed, name="task_completed")
)
