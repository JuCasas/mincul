from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.views.defaults import page_not_found

from mincul_app import views
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.template, name='template'),
    path('kit/', views.material, name='material'),
    path('patrimonios/', include('patrimonios.urls')),
    path('conservacion/', include('conservacion.urls')),
    path('incidentes/', include('incidente.urls')),
    path('reportes/', include('reportes.urls')),
    path('traslado/', include('traslado.urls')),
    path('auth/', include('authentication.urls')),
    path('mapa/',include('mapa.urls')),
    path('mapa_patrimonio/',include('mapa_patrimonio.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "mincul.views.error_404_view"
