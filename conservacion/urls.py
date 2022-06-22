from django.urls import path
from conservacion import views

urlpatterns = [
    path('proyectos/',views.listProjects, name='listProjects'),
    path('proyectos/add/',views.addProject, name='addProject'),
    path('proyectos/edit/<pk>/',views.editProject, name='addProject'),
    path('proyectos/delete/<pk>/',views.deleteProject, name='deleteProject'),
    path('proyectos/<pk>/patrimonios/',views.listPatrimonys, name='listPatrimonys'),
    path('proyectos/<pk>/patrimonios/list/',views.listPatrimonysForProject, name='listPatrimonysForProject'),
    path('proyectos/<pk>/patrimonios/add/',views.addPatrimony, name='addPatrimony'),
    path('proyectos/<pk>/patrimonios/delete/',views.deletePatrimony, name='deletePatrimony'),
    path('proyectos/<pk>/actividades/',views.listActivities, name='listActivities'),
    path('proyectos/<pk>/incidentes/',views.listIncidents, name='listIncidents'),
    path('proyectos/<pk>/actividades/add/',views.addActivity, name='addActivity'),
    path('proyectos/<pk>/actividades/edit/<pkActividad>',views.editActivity, name='editActivity'),
    path('proyectos/<pk>/actividades/delete/<pkActividad>',views.deleteActivity, name='deleteActivity'),
    path('actividades/<pk>/tareas/',views.listTasks, name='listTasks'),
    path('proyectos/patrimonios/',views.listPatrimonys_Project, name='listPatrimonys_Project'),
    path('actividades/<pk>/tareas/add/view/',views.addTaskView, name='addTaskView'),
    path('actividades/<pk>/tareas/add/',views.addTask, name='addTask'),
]