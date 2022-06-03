import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from conservacion.models import ProyectoConservacion, Actividad
from conservacion.serializers import ProyectoConservacionSerializer
from patrimonios.models import Patrimonio


def query_projects_by_args(pk, **kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]

    if(pk==-1):
        queryset = ProyectoConservacion.objects.filter(estado='1')
    else:
        patrimonio = Patrimonio.objects.get(pk=pk)
        queryset = patrimonio.proyectoconservacion_set.all()

    total = queryset.count()

    if search_value:
        queryset = queryset.filter(nombre__icontains=search_value)

    count = queryset.count()
    queryset = queryset[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }

@api_view(('GET',))
def listProjects(request,**kwargs):
    if request.is_ajax():
        project = query_projects_by_args(-1,**request.GET)
        serializer = ProyectoConservacionSerializer((project['items']),many = True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = project['total']
        result['recordsFiltered'] = project['count']
        return Response(result, status=status.HTTP_200_OK,template_name=None, content_type=None)
    else:
        return render(request,'proyectoConservacion/project_list.html')

@api_view(('POST',))
def addProject(request):
    codigo = request.POST['codigo']
    nombre = request.POST['nombre']
    fechaInicio = datetime.date.today()
    fechaFin = datetime.date.today()
    tipo = int((request.POST['tipoPlan']))
    project = ProyectoConservacion.objects.create(
        codigo = codigo,
        nombre=nombre,
        tipoProyecto=tipo,
        fechaInicio=fechaInicio,
        fechaFin=fechaFin)
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def editProject(request,pk):
    project = ProyectoConservacion.objects.get(pk=pk)
    codigo = request.POST['codigo']
    nombre = request.POST['nombre']
    tipo = int((request.POST['tipoPlan']))
    project.codigo = codigo
    project.nombre = nombre
    project.tipoProyecto = tipo
    project.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)

@api_view(('POST',))
def deleteProject(request,pk):
    project = ProyectoConservacion.objects.get(pk=pk)
    project.estado='2'
    project.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)

@api_view(('GET',))
def listActivities(request,pk):
    if request.is_ajax():
        project = ProyectoConservacion.objects.get(pk=pk)
        activities = Actividad.objects.filter(proyecto=project).filter(estado='1')
        act = list(activities)
        print(len(act))
        # project = query_projects_by_args(**request.GET)
        # serializer = ProyectoConservacionSerializer((project['items']),many = True)
        # result = dict()
        # result['data'] = serializer.data
        # result['recordsTotal'] = project['total']
        # result['recordsFiltered'] = project['count']
        return Response({}, status=status.HTTP_200_OK,template_name=None, content_type=None)
    else:
        return render(request,'proyectoConservacion/activity_list.html')

def listPatrimonys(request,**kwargs):
    context = {
        'patrimonios': Patrimonio.objects.all()
    }
    return render(request, 'proyectoConservacion/patrimony_list.html',context)

@api_view(('GET',))
def listProjects_Patrimonys(request,pk):
    context = {
        'pat': Patrimonio.objects.get(pk=pk)
    }
    if request.is_ajax():
        project = query_projects_by_args(pk,**request.GET)
        serializer = ProyectoConservacionSerializer((project['items']),many = True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = project['total']
        result['recordsFiltered'] = project['count']
        return Response(result, status=status.HTTP_200_OK,template_name=None, content_type=None)
    else:
        return render(request,'proyectoConservacion/projects_patrimony_list.html',context)