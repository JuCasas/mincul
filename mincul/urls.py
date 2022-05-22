from django.contrib import admin
from django.urls import path,include

from mincul_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.template, name='template'),
    path('kit/', views.material, name='material'),
    path('patrimonio/detalle', views.detalle, name='detalle'),
    path('', views.login, name='login'),
    path('patrimonios/', include('patrimonios.urls')),
    path('conservacion/', include('conservacion.urls')),
    path('incidente/', include('incidente.urls')),
    path('reportes/', include('reportes.urls')),
    path('traslado/', include('traslado.urls')),
    path('auth/', include('authentication.urls')),
    path('mapa/',include('mapa.urls')),
]
