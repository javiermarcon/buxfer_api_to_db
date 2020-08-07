from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('buxfer/accounts/import/', views.accounts_import),
]
