from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_system.models import Position, TaskType, Task


admin.site.register(Position)
admin.site.register(TaskType)


@admin.register(get_user_model())
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )

    search_fields = ["first_name", "last_name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    ]
    ordering = ["deadline"]
    search_fields = ["name"]
    list_filter = ["priority", "is_completed", "task_type"]

    admin.site.unregister(Group)
