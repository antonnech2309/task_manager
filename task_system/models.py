from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)


class TaskType(models.Model):
    name = models.CharField(max_length=255)
