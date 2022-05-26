import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from conservacion.models import ProyectoConservacion
from conservacion.serializers import ProyectoConservacionSerializer

# def serialize(projects_query_set):
#     return [{"id": projects_obj.id,
#              "nombre": projects_obj.nombre,
#              "descripcion": projects_obj.descripcion,
#              "fechaInicio": projects_obj.fechaInicio.strftime("%d/%m/%Y")}
#             for projects_obj in projects_query_set]

def query_projects_by_args(**kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]

    queryset = ProyectoConservacion.objects.filter(estado='1')
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
        project = query_projects_by_args(**request.GET)
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
    project = ProyectoConservacion.objects.create(
        codigo = codigo,
        nombre=nombre,
        fechaInicio=fechaInicio,
        fechaFin=fechaFin)
    #return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)
    return render(request, 'proyectoConservacion/project_list.html')