from django.urls import path
from conservacion import views

urlpatterns = [
    path('proyectos/',views.listProjects, name='listProjects'),
    path('proyectos/add/',views.addProject, name='addProject'),
    path('proyectos/edit/<pk>/',views.editProject, name='addProject'),
    path('proyectos/delete/<pk>/',views.deleteProject, name='deleteProject'),
    path('proyectos/<pk>/actvidades/',views.listActivities, name='listActivities'),
]