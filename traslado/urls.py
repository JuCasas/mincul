from django.urls import path
from traslado import views

urlpatterns = [
    #path('',views.listProjects, name='listTransfer'),
    path('add/',views.addTransfer, name='addTransfer'),
    path('entidades/', views.listEntidades, name='listEntidades'),
    path('eliminarSolicitantes/<id>',views.eliminarSolicitantes, name='eliminarSolicitantes'),
    path('eliminarEntidad/<id>',views.eliminarEntidad,name='eliminarEntidad')
]