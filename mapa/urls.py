from django.urls import path, include

from mapa import views

urlpatterns = [
    path('ficha/<my_id>/',views.ficha,name='ficha'),
    path('buscarpatrimoniosimple',views.mapaPatrimonioSimple,name='mapaPatrimonioSimple'),
    path('buscarpatrimonioavanzado',views.mapaPatrimonioAvanzado,name='mapaPatrimonioAvanzado'),
]