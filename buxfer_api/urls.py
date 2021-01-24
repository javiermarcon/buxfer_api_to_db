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
    path('planilla', views.planilla_estado_financiero),
    path('planilla/<int:anio>', views.planilla_estado_financiero),
    path('planilla/<int:anio>/<int:mes>', views.planilla_estado_financiero),
    path('cotizacion/dolar/todos', views.precios_dolar, {'modo': 'todos'}),
    path('cotizacion/dolar/actualizar', views.precios_dolar, {'modo': 'actualizar'}),
    path('cotizacion/dolar/<int:anio>/<int:mes>/<int:dia>', views.precios_dolar, {'modo': 'fecha'}),

    # https://github.com/alsoicode/django-admin-sortable
    # https://github.com/venmo/business-rules
    # https://github.com/venmo/business-rules-ui
]
