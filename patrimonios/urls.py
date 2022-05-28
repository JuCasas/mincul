from django.urls import path, include

from patrimonios import views

urlpatterns = [
    path('listar/', views.patrimonio_list, name='patrimonio_list'),
    path('gestor/', views.patrimonio_gestor, name='patrimonio_gestor'),
]
