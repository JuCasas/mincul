from django.urls import path, include

from patrimonios import views

urlpatterns = [
    path('listar/', views.patrimonio_list, name='patrimonio_list'),
    path('edit/<pk>', views.patrimonio_edit, name='patrimonio_edit'),
    path('detalle/<pk>', views.detalle, name='detalle'),
    path('email_confirmation/<pk>', views.email_confirmation, name='email'),
    path('listarInstituciones/',views.instituciones_list_api, name='instituciones_list_api'),
    path('listarGestorPatrimonio/',views.gestorPatrimonio_list_api, name='gestorPatrimonio_list_api'),
    path('detalle/area/<pk>', views.detalle_museo, name='detalle_museo'),
    path('detalle/area/valor/<pk>', views.valor_museo, name='valor_museo'),
    path('detalle/area/incidente/<pk>', views.incidete_museo, name='incidete_museo'),
]
