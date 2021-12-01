from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import date
from datetime import timedelta
from .serializers import TaskSerializer, AlarmSerializer
from .models import Task, Alarm
# Create your views here.

# View Task


class TaskView(viewsets.ViewSet):
    """
    This view lists, creates ans destroy tasks
    """
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Task.objects.all().filter(user=request.user)
        serializer = TaskSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk)

            if(task.user != request.user):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Http404:
            return Response(data={'error': 'Objects doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk)

            if task.user == request.user:
                task.delete()
        except Http404:
            return Response(data={'error': 'Object doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk)

            if task.user != request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(data=request.data)

            if serializer.is_valid():
                task = serializer.save()
                task.save()
            else:
                return Response(data={'error': 'Request invalid'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        except Http404:
            return Response(data={'error': 'Object doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# Alarm view
class AlarmView(viewsets.ViewSet):
    """
    This view lists, creates ans destroy tasks
    """
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Alarm.objects.all().filter(user=request.user)
        query = []

        for q in queryset:
            time_now = timezone.now()
            time = time_now - q.alarm_date

            if time <= timedelta(days=2):
                query.append(q)

        serializer = AlarmSerializer(query, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            alarm = get_object_or_404(Alarm, pk=pk)

            if(alarm.user != request.user):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = AlarmSerializer(alarm)
            return Response(serializer.data)
        except Http404:
            return Response(data={'error': 'Objects doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            alarm = get_object_or_404(Alarm, pk=pk)

            if alarm.user == request.user:
                alarm.delete()
        except Http404:
            return Response(data={'error': 'Object doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try:
            alarm = get_object_or_404(Alarm, pk=pk)

            if alarm.user != request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(data=request.data)

            if serializer.is_valid():
                alarm = serializer.save()
                alarm.save()
            else:
                return Response(data={'error': 'Request invalid'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        except Http404:
            return Response(data={'error': 'Object doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = AlarmSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# Check Tasks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_tasks(request):
    """
    This view checks if dead_line is 3 days or more over
    the dead_line  
    """

    tasks = Task.objects.all().filter(user=request.user)
    date_now = date.today()
    count = 0

    for t in tasks:
        time = date_now - t.dead_line
        if time >= timedelta(days=3):
            t.delete()
            count += 1

    return Response(data={'Deleted': count})


# Check alarms
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_alarms(request):
    """
    This view check if alarm_date is over 3 days from today
    """

    alarms = Alarm.objects.all().filter(user=request.user)
    time_now = timezone.now()
    count = 0

    for a in alarms:
        time = time_now - a.alarm_date
        if time >= timedelta(days=3):
            count += 1
            a.delete()

    return Response(data={'Deleted': count})
