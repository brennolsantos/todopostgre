from rest_framework import serializers
from .models import Task, Alarm


# Serializer task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# Serializer alarm
class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'
