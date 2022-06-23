from django.urls import path, include

from mapa import views

urlpatterns = [
    path('ficha/<my_id>/',views.ficha,name='ficha'),
    path('buscarpatrimoniosimple',views.mapaPatrimonioSimple,name='mapaPatrimonioSimple'),
    path('buscarpatrimonioavanzado',views.mapaPatrimonioAvanzado,name='mapaPatrimonioAvanzado'),
    path('provinciajson/<id_representativo>', views.provinciaJson, name='provinciaJson'),
    path('distritojson/<id_representativo>', views.distritoJson, name='distritoJson'),
    path('patrimoniojson/<id_patrimonio>', views.patrimonioJson, name='patrimonioJson'),
    path('institucionjson/<id_institucion>', views.institucionJson, name='institucionJson'),
]