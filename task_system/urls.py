from django.urls import path

from task_system.views import index, WorkerDetailView, WorkerCreateView

urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
]

app_name = "task_system"
