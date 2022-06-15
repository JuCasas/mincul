from django.urls import path, include

from mapa import views

urlpatterns = [
    path('ficha/<my_id>/',views.ficha,name='ficha'),
    path('buscarpatrimonios',views.mapaPatrimonio,name='mapaPatrimonio'),
]