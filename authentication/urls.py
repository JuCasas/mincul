from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from authentication import views

urlpatterns = [
    # path( url hijo, backend, nombre de la variable)
    path('login/', views.signin, name="signin"),
    path('login/?/', views.signout, name="signout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
