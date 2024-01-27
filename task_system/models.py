from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return (f"{self.username} ({self.first_name} "
                f"{self.last_name} {self.position.name})")


class Task(models.Model):
    URGENT = "Urgent"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    ROUTINE = "Routine"
    TASK_PRIORITY_CHOICES = [
        (URGENT, "Urgent"),
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        (ROUTINE, "Routine"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=20,
        choices=TASK_PRIORITY_CHOICES,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(get_user_model(), related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return f"{self.name} ({self.task_type.name} {self.get_priority_display()})"
