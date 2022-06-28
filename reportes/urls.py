from django.urls import path, include

from reportes import views

urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('traerData/', views.traerData, name='traerData'),
]