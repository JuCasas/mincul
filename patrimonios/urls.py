from django.urls import path, include

from patrimonios import views

urlpatterns = [
    path('listar/', views.patrimonio_list, name='patrimonio_list'),
    path('edit/<pk>', views.patrimonio_edit, name='patrimonio_edit'),
]
