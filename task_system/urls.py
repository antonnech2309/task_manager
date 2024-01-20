from django.urls import path

from task_system.views import (
    index,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskListView,
    TaskUpdateView,
    TaskCreateView,
    TaskDetailView,
    TaskDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/detail",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/<int:pk>/delete",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
]

app_name = "task_system"
