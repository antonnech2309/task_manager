from django.urls import path

from task_system.views import index, WorkerDetailView

urlpatterns = [
    path("", index, name="index"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]

app_name = "task_system"
