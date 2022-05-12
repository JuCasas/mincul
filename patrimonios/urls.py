from django.urls import path, include

from patrimonios import views

urlpatterns = [
    path('listar/', views.patrimony_list, name='patrimony_list'),
]
