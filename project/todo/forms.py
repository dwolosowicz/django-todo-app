from django import forms
from .models import Task, UserProfile
from django.contrib.auth.models import User
from timezone_field import TimeZoneFormField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['timezone']


class TaskContentForm(forms.ModelForm):
    content = forms.CharField(min_length=20, required=True)

    class Meta:
        model = Task
        fields = ['content']

class TaskForm(forms.ModelForm):
    content = forms.CharField(min_length=20, required=True, widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['content', 'priority']
