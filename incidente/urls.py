from django.urls import path, include

from incidente import views

urlpatterns = [
    path('listar/', views.incidente_listar, name='incidente_listar'),
    path('listar/detalle/', views.incidente_detalles, name='incidente_detalles'),

]