from django.urls import path, include
from rest_framework import routers
from .views import TaskView, AlarmView, check_alarms, check_tasks

app_name = 'notes'

router = routers.DefaultRouter()
router.register(r'tasks', TaskView, basename='task')
router.register(r'alarms', AlarmView, basename='alarm')

urlpatterns = [
    path('check-tasks', check_tasks, name='check-tasks'),
    path('check-alarms', check_alarms, name='check_alarms'),
    path('', include(router.urls))
]
