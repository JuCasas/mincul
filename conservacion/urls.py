from django.urls import path, include

from conservacion import views

urlpatterns = [
    path('proyectos/',views.listProjects, name='listProjects'),
    path('proyectos/add/',views.addProject, name='addProject'),
]