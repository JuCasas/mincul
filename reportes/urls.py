from django.urls import path, include

from reportes import views

urlpatterns = [
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/traerData', views.traerData, name='traerData'),
    path('reportes/traerNombres', views.traerNombres, name='traerNombres'),
]