from django.urls import path
from traslado import views

urlpatterns = [
    #path('',views.listProjects, name='listTransfer'),
    path('agregar/',views.addTransfer, name='addTransfer'),
    path('listar/',views.listTranfers, name='list_transfers'),
    path('ver/<int:pk>/', views.viewTranfer, name='view_transfer'),
    path('editar/<int:pk>/', views.editTransfer, name='edit_transfer'),

]