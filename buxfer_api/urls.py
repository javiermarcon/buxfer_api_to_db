from django.urls import include, path, re_path
# from rest_framework import routers
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
    path('cotizacion/dolar/add/todos', views.add_precios_dolar, {'modo': 'todos'}),
    path('cotizacion/dolar/add/actualizar', views.add_precios_dolar, {'modo': 'actualizar'}),
    path('cotizacion/dolar/add/<int:anio>/<int:mes>/<int:dia>', views.add_precios_dolar, {'modo': 'fecha'}),
    path('convertir/<moneda_origen>/<moneda_destino>/<int:anio>/<int:mes>/<int:dia>/<int:cantidad>', views.convertir_moneda, {'impuesto_pais': True}),
    path('convertir/noi/<moneda_origen>/<moneda_destino>/<int:anio>/<int:mes>/<int:dia>/<int:cantidad>', views.convertir_moneda, {'impuesto_pais': True}),
    re_path(r"^convertir/(?P<moneda_origen>\w)/(?P<moneda_destino>\w)/(?P<anio>\d)/(?P<mes>\d)/(?P<dia>\d)/(?P<cantidad>\d+\.\d+)$", views.convertir_moneda, {'impuesto_pais': True}),
    re_path(r"^convertir/noi/(?P<moneda_origen>[A-Za-z]+)/(?P<moneda_destino>[A-Za-z]+)/(?P<anio>\d)/(?P<mes>\d)/(?P<dia>\d)/(?P<cantidad>\d+\.\d+)$", views.convertir_moneda, {'impuesto_pais': False}),
    # https://github.com/alsoicode/django-admin-sortable
    # https://github.com/venmo/business-rules
    # https://github.com/venmo/business-rules-ui
]
