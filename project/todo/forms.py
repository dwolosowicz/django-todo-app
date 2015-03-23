from django import forms
from .models import Task

class TaskForm(forms.Form):
    pass

class TaskContentForm(forms.Form):
    content = forms.CharField(required=True, min_length=20)

class TaskPriorityForm(forms.Form):
    priority = forms.ChoiceField(choices=Task.PRIORITIES)

class TaskCompletedForm(forms.Form):
    is_completed = forms.BooleanField()
