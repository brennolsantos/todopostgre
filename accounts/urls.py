from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import RegisterView

router = routers.DefaultRouter()
router.register(r'register', RegisterView, basename='register')

app_name = 'accounts'

urlpatterns = [
    path('token-auth', views.obtain_auth_token),
    path('', include(router.urls))
]
