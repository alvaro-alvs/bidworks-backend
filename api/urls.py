

from django.urls import path
from .views.views import HealthCheck, CreateUser

urlpatterns = [
    path('', HealthCheck, name='HealthCheck'),
    path('sign-up/', CreateUser, name='signup'),
]