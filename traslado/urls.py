from django.urls import path
from traslado import views

urlpatterns = [

    path('agregar/',views.addTransfer, name='addTransfer'),
    path('listar/',views.listTranfers, name='list_transfers'),
    path('ver/<int:pk>/', views.viewTranfer, name='view_transfer'),
    path('editar/<int:pk>/', views.editTransfer, name='edit_transfer'),
    path('editarEstado/', views.actualizarEstado, name='actualizar_estado'),
    path('editarEstado2/', views.actualizarEstado2, name='actualizar_estado_2'),
    path('patrimonioAjax/',views.listarPatrimoniosTraslado,name='listPatrimoniosAjax'),
    
    
    path('entidades/', views.listEntidades, name='listEntidades'),
    path('eliminarSolicitantes/<id>',views.eliminarSolicitantes, name='eliminarSolicitantes'),
    path('registrarSolicitantes/',views.registrarSolicitantes,name='registrarSolicitantes'),
    path('editarSolicitante/',views.editarSolicitante,name='editarSolicitante'),
    path('eliminacionSolicitante/',views.eliminacionSolicitante,name='eliminacionSolicitante'),
    path('emailEntidad/',views.entidadEmail,name='entidadEmail'),
    path('validarResolucion/',views.validarResolucion,name='validarResolucion'),
    path('registrarNumResolucion/',views.registrarNumResolucion,name='registrarNumResolucion'),
    path('registrarFechaSalidaReal/',views.registrarFechaSalidaReal,name='registrarFechaSalidaReal'),
    path('registrarFechaRetornoReal/',views.registrarFechaRetornoReal,name='registrarFechaRetornoReal'),
    path('eliminarDocumentoTraslado/',views.eliminarDocumentoTraslado,name='eliminarDocumentoTraslado'),
    path('validarDOI/',views.validarDOI,name="validarDOI"),
    path('validarFechas/',views.validarFechas,name="validarFechas"),
    path('existeResolucion/',views.existeResolucion,name="existeResolucion"),
    path ('existeFechaSalidaProgramada/',views.existeFechaSalidaProgramada,name="existeFechaSalidaProgramada"),
    path ('existeFechaSalidaReal/',views.existeFechaSalidaReal,name="existeFechaSalidaReal"),
    path ('existeFechaRetornoReal/',views.existeFechaRetornoReal,name="existeFechaRetornoReal"),
]