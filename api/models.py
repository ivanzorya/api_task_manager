from django.contrib.auth.models import User
from django.db import models


class Status(models.TextChoices):
    NEW = 'new'
    PLANNED = 'planned'
    WORK = 'work'
    COMPLETED = 'completed'


class Task(models.Model):
    title = models.TextField(
        verbose_name='task title',
        max_length=100
    )
    description = models.TextField(
        verbose_name='description',
        max_length=1000)
    created = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name="created date"
    )
    completed = models.DateField(
        db_index=True,
        verbose_name="planed completed date",
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="author")
    status = models.CharField(
        verbose_name='task status',
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Change(models.Model):
    task = models.ForeignKey(
        Task,
        verbose_name='task id',
        related_name="changes",
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    field_name = models.TextField(
        verbose_name='change data',
        max_length=1000
    )
    old_value = models.TextField(
        verbose_name='change data',
        max_length=1000
    )
    new_value = models.TextField(
        verbose_name='change data',
        max_length=1000
    )
    author = models.ForeignKey(
        User, verbose_name='author',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='date of change',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["pub_date"]

    def __str__(self):
        return (f'{self.field_name} changed, '
                f'from {self.old_value} to {self.new_value}')
