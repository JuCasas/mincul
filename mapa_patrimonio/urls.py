from django.urls import path, include

from mapa_patrimonio import views as mapa_patrimonio_views

urlpatterns = [
    path('mapa/index', mapa_patrimonio_views.index, name='index'),
    path('mapa/datos', mapa_patrimonio_views.datos, name='datos')
]