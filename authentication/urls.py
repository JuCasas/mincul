from django.contrib import admin
from django.urls import path, include

from authentication import views

urlpatterns = [
    # path( url hijo, backend, nombre de la variable)
    path('login/', views.RenderLogin.as_view(), name="login"),
]
