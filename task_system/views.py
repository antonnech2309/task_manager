from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_system.forms import WorkerCreationForm, TaskForm
from task_system.models import Task, Position


@login_required
def index(request):
    """View function for the home page of the site."""

    num_users = get_user_model().objects.count()
    tasks = Task.objects.all()
    num_tasks = len(tasks)
    num_active_tasks = Task.objects.filter(is_completed=False).count()
    num_user_tasks = request.user.tasks.count()
    num_user_active_tasks = request.user.tasks.filter(is_completed=False).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    percentage_all_tasks = 0
    percentage_user_tasks = 0

    if num_tasks != 0:
        percentage_all_tasks = round(num_active_tasks / num_tasks * 100)

    if num_user_tasks != 0:
        percentage_user_tasks = round(
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

    return render(request, "task_system/index.html", context=context)


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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5


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
