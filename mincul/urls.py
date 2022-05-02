from django.contrib import admin
from django.urls import path

from mincul_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.template, name='template'),
    path('login/', views.login, name='login'),
]
