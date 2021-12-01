from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RegisterSerializer
from django.contrib.auth.models import User


class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
