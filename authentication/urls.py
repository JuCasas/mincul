from django.contrib import admin
from django.urls import path, include
from mincul import urls
from authentication import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path( url hijo, backend, nombre de la variable)
    path('login2/', LoginView.as_view(template_name='aux_login.html'), name="login2"),
    path('logout/', views.logoutUsuario,name='logout'),
    path('register/', login_required(views.registe), name="register"),
]
