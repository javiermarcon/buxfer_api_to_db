from django.urls import path
from . import views

urlpatterns = [
    path('buxfer/accounts/import/', views.accounts_import),
]