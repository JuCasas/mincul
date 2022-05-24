from django.urls import path, include

from conservacion import views

urlpatterns = [
    path('',views.Show, name='showProjects'),
]