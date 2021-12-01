from django.contrib import admin
from .models import Task, Alarm


admin.site.register(Task)
admin.site.register(Alarm)

# Register your models here.
