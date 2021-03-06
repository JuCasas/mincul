from django.urls import path
from conservacion import views

urlpatterns = [
    path('proyectos/', views.listProjects, name='listProjects'),
    path('proyectos/add/', views.addProject, name='addProject'),
    path('proyectos/edit/<pk>/', views.editProject, name='addProject'),
    path('proyectos/delete/<pk>/', views.deleteProject, name='deleteProject'),
    path('proyectos/<pk>/patrimonios/', views.listPatrimonys, name='listPatrimonys'),
    path('proyectos/<pk>/patrimonios/list/', views.listPatrimonysForProject, name='listPatrimonysForProject'),
    path('proyectos/<pk>/patrimonios/add/', views.addPatrimony, name='addPatrimony'),
    path('proyectos/<pk>/patrimonios/delete/', views.deletePatrimony, name='deletePatrimony'),
    path('proyectos/<pk>/patrimonios/verify/', views.verifyPatrimony, name='verifyPatrimony'),

    path('proyectos/<pk>/actividades/', views.listActivities, name='listActivities'),
    path('proyectos/<pk>/incidentes/', views.listIncidents, name='listIncidents'),

    path('proyectos/<pk>/actividades/add/', views.addActivity, name='addActivity'),
    path('proyectos/<pk>/actividades/add/view/', views.addActivityView, name='addActivityView'),
    path('proyectos/<pk>/actividades/edit/<pkActividad>/view/', views.editActivityView, name='editActivityView'),
    path('proyectos/<pk>/actividades/edit/<pkActividad>', views.editActivity, name='editActivity'),
    path('proyectos/<pk>/actividades/delete/<pkActividad>', views.deleteActivity, name='deleteActivity'),
    path('actividades/<pk>/tareas/', views.listTasks, name='listTasks'),
    path('actividades/validateEndActivity/', views.validateEndActivity, name='validateEndActivity'),


    path('proyectos/patrimonios/', views.listPatrimonys_Project, name='listPatrimonys_Project'),
    path('proyectos/patrimonios_actividad/', views.listPatrimonys_Activity, name='listPatrimonys_Activity'),

    path('actividades/<pk>/tareas/add/view/', views.addTaskView, name='addTaskView'),
    path('actividades/<pk>/tareas/add/', views.addTask, name='addTask'),
    path('actividades/updateState/', views.updateActivityState, name='updateActivityState'),
    path('proyecto/updateState/', views.updateProjectState, name='updateProjectState'),
    path('tareas/edit/<pk>/', views.editTask, name='editTask'),
    path('tareas/edit/<pk>/addSection/', views.addSection, name='addSection'),
    path('tareas/edit/<pk>/listSections/', views.listSections, name='listSections'),
    path('tareas/updateState/', views.updateTaskState, name='updateTaskState'),
    path('tareas/updateState2/', views.updateTaskState2, name='updateTaskState2'),
    path('tareas/editView/<pk>/', views.editTaskView, name='editTaskView'),
    path('tareas/deleteSection/', views.deleteSection, name="deteleSection"),
    path('tareas/validateExistSections/', views.validateSections, name="validateSections"),
    path('tareas/detailView/<pk>/', views.detailTaskView, name='detailTaskView'),
    path('actividades/conservadores/', views.addConservador, name='addConservador'),
    path('actividades/relaciones/<pk>', views.addRelacion, name='addRelacion'),
    path('eliminarDocumentoActividad/', views.eliminarDocumentoActividad, name='eliminarDocumentoActividad'),
]
