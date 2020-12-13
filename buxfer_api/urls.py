from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('buxfer/accounts/import/', views.accounts_import),
    path('buxfer/tags/import/', views.tags_import),
    path('buxfer/transactions/import/', views.transactions_import),
    path('view/cuadro_activos', views.cuadro_activos),
    path('view/cuadro_activos/<int:anio>', views.cuadro_activos),
    path('view/cuadro_activos/<int:anio>/<int:mes>', views.cuadro_activos),

    # https://github.com/alsoicode/django-admin-sortable
    # https://github.com/venmo/business-rules
    # https://github.com/venmo/business-rules-ui
]
