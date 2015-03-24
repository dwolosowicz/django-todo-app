from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core import mail

from .models import Task, UserProfile
from django.contrib.auth.models import User

from .forms import UserProfileForm, UserForm, TaskForm, TaskContentForm


def get_user_object_or_404(entity, user, **kwargs):
    return get_object_or_404(entity.objects.filter(user=user), **kwargs)


class IndexView(generic.ListView):
    template_name = "todo/index.html"
    queryset = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user,
            is_completed=False).order_by('-created')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def register(request):
    form = UserForm(instance=User())
    profile_form = UserProfileForm(instance=UserProfile())

    if request.method == "POST":
        form = UserForm(request.POST, instance=User())
        profile_form = UserProfileForm(request.POST, instance=UserProfile())

        if form.is_valid() and profile_form.is_valid():
            user = form.save(False)
            user.set_password(user.password)
            user.save()

            user_profile = user.user_profile
            user_profile.timezone = profile_form.cleaned_data['timezone']
            user_profile.save()

            mail.send_mail(
                    "Good job with creating your account on PersonalTodos!",
                    "You've successfully created an account on PersonalTodos. Don't wait, create your todo list right away!",
                    "account@personaltodos.com",
                    [ user.email ],
                    fail_silently=True
                    )

            return redirect(reverse('login'))

    return render(request, 'registration/registration.html', {
        'form': form,
        'profile_form': profile_form
    })


@login_required
def task(request):
    template = 'todo/new.html'
    form = TaskForm(instance=Task())

    if request.method == "POST":
        form = TaskForm(request.POST, instance=Task())

        if form.is_valid():
            task = form.save(False)
            task.user = request.user
            task.save()

            return redirect(reverse('index'))

    return render(request, template, {'form': form})


def __task_update_field(form, user):
    if form.is_valid():
        form.save()

        return HttpResponse()
    else:
        return HttpResponse(status=400)


@login_required
def task_content(request):
    task = get_user_object_or_404(Task, request.user, pk=request.POST['id'])

    return __task_update_field(TaskContentForm(request.POST, instance=task), request.user)


@login_required
def task_priority(request):
    task = get_user_object_or_404(Task, request.user, pk=request.POST['id'])
    Form = modelform_factory(Task, fields=['priority'])

    return __task_update_field(Form(request.POST, instance=task), request.user)


@login_required
def task_completed(request):
    task = get_user_object_or_404(Task, request.user, pk=request.POST['id'])
    Form = modelform_factory(Task, fields=['is_completed'])

    return __task_update_field(Form(request.POST, instance=task), request.user)

@login_required
def task_remove(request):
    task = get_user_object_or_404(Task, request.user, pk=request.POST['id'])
    task.delete()

    return HttpResponse()
