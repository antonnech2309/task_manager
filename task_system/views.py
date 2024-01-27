from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_system.forms import (
    WorkerCreationForm,
    TaskForm,
    WorkerUsernameSearchForm
)
from task_system.models import Task, Position, TaskType


def round_to_5_or_0(number):
    return round(number / 5) * 5


@login_required
def index(request):
    """View function for the home page of the site."""

    num_users = get_user_model().objects.count()
    tasks = Task.objects.all()
    num_tasks = len(tasks)
    num_active_tasks = Task.objects.filter(is_completed=False).count()
    num_user_tasks = request.user.tasks.count()
    num_user_active_tasks = request.user.tasks.filter(
        is_completed=False
    ).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    percentage_all_tasks = 0
    percentage_user_tasks = 0

    if num_tasks != 0:
        percentage_all_tasks = round_to_5_or_0(
            num_active_tasks / num_tasks * 100
        )

    if num_user_tasks != 0:
        percentage_user_tasks = round_to_5_or_0(
            num_user_active_tasks /
            num_user_tasks * 100
        )

    context = {
        "num_tasks": num_tasks,
        "num_users": num_users,
        "num_visits": num_visits + 1,
        "tasks": tasks,
        "percentage_all_tasks": percentage_all_tasks,
        "percentage_user_tasks": percentage_user_tasks,
        "num_active_tasks": num_active_tasks,
        "num_user_active_tasks": num_user_active_tasks,
    }

    return render(
        request,
        "task_system/index.html",
        context=context
    )


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = "/"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    fields = ["first_name", "last_name", "position", "username", "email"]
    success_url = reverse_lazy("task_system:index")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_system:index")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5
    template_name = "task_system/worker_list.html"
    context_object_name = "worker_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            WorkerListView,
            self
        ).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all().select_related(
            "position"
        )
        form = WorkerUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        user_filter = self.request.GET.get('user', None)

        if user_filter == 'mine':
            return user.tasks.all().select_related("task_type")
        return Task.objects.all().select_related("task_type")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    success_url = reverse_lazy("task_system:task-list")
    form_class = TaskForm


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    success_url = reverse_lazy("task_system:task-list")
    form_class = TaskForm


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related(
        "assignees"
    ).select_related("task_type")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_system:task-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_system:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_system:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_system:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_system:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_system:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_system:task-type-list")
