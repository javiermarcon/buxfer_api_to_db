from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('buxfer/accounts/import/', views.accounts_import),
    path('buxfer/tags/import/', views.tags_import),
    path('buxfer/transactions/import/', views.transactions_import),
]
