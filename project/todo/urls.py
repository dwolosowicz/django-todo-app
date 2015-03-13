from django.conf.urls import url, patterns
from todo import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="index")
)