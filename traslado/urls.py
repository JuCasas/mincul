from django.urls import path
from traslado import views

urlpatterns = [
    #path('',views.listProjects, name='listTransfer'),
    # path('add/',views.addTransfer, name='addTransfer'),
    path('agregar/',views.addTransfer, name='addTransfer'),
    path('listar/',views.listTranfers, name='list_transfers'),
    path('ver/<int:pk>/', views.viewTranfer, name='view_transfer'),
    path('editar/<int:pk>/', views.editTransfer, name='edit_transfer'),
    path('patrimonioAjax/',views.listarPatrimoniosTraslado,name='listPatrimoniosAjax'),
    
    
    path('entidades/', views.listEntidades, name='listEntidades'),
    path('eliminarSolicitantes/<id>',views.eliminarSolicitantes, name='eliminarSolicitantes'),
    path('registrarSolicitantes/',views.registrarSolicitantes,name='registrarSolicitantes'),
    path('editarSolicitante/',views.editarSolicitante,name='editarSolicitante')
]