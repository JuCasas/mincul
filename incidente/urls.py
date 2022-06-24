from django.urls import path, include

from incidente import views

urlpatterns = [
    path('', views.patrimonio_incidente_listar, name='patrimonio_incidente_listar'),
    path('<pk>/detalle/', views.incidente_detalle, name='incidente_detalle'),
    path('zonas/', views.listar_zonas, name='listar_zonas'),
    path('listar/<patrimonio_pk>/', views.incidente_reporte_listar, name='incidente_reporte_listar'),
    path('listar/<patrimonio_pk>/agregar', views.incidente_reporte_agregar, name='incidente_reporte_agregar'),
    path('listar/<patrimonio_pk>/reporte/<incidente_pk>', views.incidente_reporte, name='incidente_reporte'),
    path('listar/<patrimonio_pk>/reporte/<incidente_pk>/modificar', views.incidente_reporte_modificar, name='incidente_reporte_modificar'),

]