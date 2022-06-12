from django.urls import path
from conservacion import views

urlpatterns = [
    path('proyectos/',views.listProjects, name='listProjects'),
    path('proyectos/add/',views.addProject, name='addProject'),
    path('proyectos/edit/<pk>/',views.editProject, name='addProject'),
    path('proyectos/delete/<pk>/',views.deleteProject, name='deleteProject'),
    path('proyectos/<pk>/actividades/',views.listActivities, name='listActivities'),
    path('proyectos/<pk>/patrimonios/',views.listPatrimonys, name='listPatrimonys'),
    path('proyectos/<pk>/actividades/add/',views.addActivity, name='addActivity'),
    path('actividades/<pk>/tareas/',views.listTasks, name='listTask'),
    path('proyectos/patrimonios/',views.listPatrimonys_Project, name='listPatrimonys_Project')
    #path('actividades/<pk>/tareas/add/',views.addTask, name='addTask'),
]