from django.urls import path, include

from mapa import views

urlpatterns = [
    path('mapaficha/', views.mapaficha, name='mapaficha'),
]