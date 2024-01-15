from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic

from task_system.models import Task


def index(request):
    """View function for the home page of the site."""

    num_tasks = Task.objects.count()
    num_users = get_user_model().objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tasks": num_tasks,
        "num_users": num_users,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_system/index.html", context=context)
