from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from task_system.models import Position, TaskType, Task


admin.site.register(Position)
admin.site.register(TaskType)
