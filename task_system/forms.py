from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from task_system.models import Task


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    deadline = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.DateTimeInput(attrs={"placeholder": "YYYY-MM-DD HH:MM"})
    )

    class Meta:
        model = Task
        fields = "__all__"
