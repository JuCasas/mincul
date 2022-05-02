from django.contrib import admin
from django.urls import path

from mincul_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.template, name='template'),
    path('kit/', views.material, name='material'),
    path('', views.login, name='login'),
]
