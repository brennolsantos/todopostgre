from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey

# Create your models here.

User = get_user_model()

# Task


class Task(models.Model):
    """
    Task
    This objects provides a to-do task, wich will appears in
    the page anytime, unless it is 3 days later of its dead_line
    """
    title = models.CharField('Task', max_length=100, blank=True)
    desc = models.TextField('Desc', max_length=1000, blank=True)
    dead_line = models.DateField('Finish', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['title']


class Alarm(models.Model):
    """
    Alarm
    The alarm only shows in page if it is on up-to 3 days its 
    alarm_date, if the timezone.now is less than its date, the alarm
    will not appear
    """
    title = models.CharField('Alarm', max_length=100, blank=True)
    desc = models.TextField('ToDo', max_length=1000, blank=True)
    alarm_date = models.DateTimeField('ToAlarm', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Alarm'
        verbose_name_plural = 'Alarms'
        ordering = ['alarm_date']
