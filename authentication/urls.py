from django.contrib import admin
from django.urls import path, include
from mincul import urls
from authentication import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    # path( url hijo, backend, nombre de la variable)
    path('login2/', LoginView.as_view(template_name='aux_login.html'), name="login2"),
    path('logout/', LogoutView.as_view(template_name='aux_login.html'), name="logout"),
    path('register/', views.registe, name="register"),
]
