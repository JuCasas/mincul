import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from conservacion.models import ProyectoConservacion, Actividad, Tarea
from conservacion.serializers import ProyectoConservacionSerializer, ActividadSerializer, TareaSerializer, \
    PatrimonioSerializer
from patrimonios.models import Patrimonio



def query_projects_by_args(**kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]
    type_filter = kwargs.get('type_filter', None)[0]
    status_filter = kwargs.get('status_filter', None)[0]
    patrimony_filter = kwargs.get('patrimony_filter', None)[0]
    order_column = kwargs.get('order_column', None)[0]
    order = kwargs.get('order', None)[0]
    if(len(patrimony_filter)==0):
        queryset = ProyectoConservacion.objects.filter(estado='1')
    else:
        patrimonio = Patrimonio.objects.get(pk=int(patrimony_filter))
        queryset = patrimonio.proyectoconservacion_set.all().filter(estado='1')

    total = queryset.count()

    order_column = ProyectoConservacion.ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column

    if search_value:
        queryset = queryset.filter(nombre__icontains=search_value)
    if type_filter:
        queryset = queryset.filter(tipoProyecto=type_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }

def query_activities_by_args(pk, **kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    # search_value = kwargs.get('search_value', None)[0]
    # type_filter = kwargs.get('type_filter', None)[0]
    # status_filter = kwargs.get('status_filter', None)[0]
    # order_column = kwargs.get('order_column', None)[0]
    # order = kwargs.get('order', None)[0]


    project = ProyectoConservacion.objects.get(pk=pk)
    queryset = Actividad.objects.filter(proyecto=project).filter(estado='1')

    total = queryset.count()

    # order_column = ProyectoConservacion.ORDER_COLUMN_CHOICES[order_column]
    # if order == 'desc':
    #     order_column = '-' + order_column
    #
    # if search_value:
    #     queryset = queryset.filter(nombre__icontains=search_value)
    # if type_filter:
    #     queryset = queryset.filter(tipoProyecto=type_filter)
    # if status_filter:
    #     queryset = queryset.filter(status=status_filter)

    count = queryset.count()
    queryset = queryset[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }

def query_tasks_by_args(pk, **kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    # search_value = kwargs.get('search_value', None)[0]
    # type_filter = kwargs.get('type_filter', None)[0]
    # status_filter = kwargs.get('status_filter', None)[0]
    # order_column = kwargs.get('order_column', None)[0]
    # order = kwargs.get('order', None)[0]


    activity = Actividad.objects.get(pk=pk)
    queryset = Tarea.objects.filter(proyecto=activity).filter(estado='1')

    total = queryset.count()

    # order_column = ProyectoConservacion.ORDER_COLUMN_CHOICES[order_column]
    # if order == 'desc':
    #     order_column = '-' + order_column
    #
    # if search_value:
    #     queryset = queryset.filter(nombre__icontains=search_value)
    # if type_filter:
    #     queryset = queryset.filter(tipoProyecto=type_filter)
    # if status_filter:
    #     queryset = queryset.filter(status=status_filter)

    count = queryset.count()
    queryset = queryset[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }

@api_view(('GET',))
def listPatrimonys_Project(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page-1)*length
    end = start + length
    queryset = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=search).order_by('nombreTituloDemoninacion')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = PatrimonioSerializer(queryset,many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


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
        context ={
            'status_choices' : ProyectoConservacion.STATUS,
            'typeProjects' : ProyectoConservacion.TIPOS
        }
        return render(request,'proyectoConservacion/project_list.html',context)

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
        activity = query_activities_by_args(pk,**request.GET)
        serializer = ActividadSerializer((activity['items']),many = True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = activity['total']
        result['recordsFiltered'] = activity['count']
        return Response(result, status=status.HTTP_200_OK,template_name=None, content_type=None)
    else:
        context = {
            'project': ProyectoConservacion.objects.get(pk=pk),
            'patrimonios': Patrimonio.objects.all()
        }
        return render(request,'proyectoConservacion/activity_list.html',context)


@api_view(('GET',))
def listPatrimonys(request,pk):
    context = {
        'project': ProyectoConservacion.objects.get(pk=pk),
        'patrimonios': Patrimonio.objects.all()
    }
    return render(request, 'proyectoConservacion/patrimonys_list.html', context)

@api_view(('GET',))
def listTasks(request,pk):
    if request.is_ajax():
        task = query_tasks_by_args(pk,**request.GET)
        serializer = TareaSerializer((task['items']),many = True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = task['total']
        result['recordsFiltered'] = task['count']
        return Response(result, status=status.HTTP_200_OK,template_name=None, content_type=None)
    else:
        context = {
            'activity': Actividad.objects.get(pk=pk),
            'project': Actividad.objects.get(pk=pk).proyecto
        }
        return render(request,'proyectoConservacion/task_list.html',context)

@api_view(('POST',))
def addActivity(request,pk):
    codigo = "ACT00"
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    fechaInicio = datetime.datetime.strptime(request.POST['fechaInicio'], "%Y-%m-%d").date()
    fechaFin = datetime.datetime.strptime(request.POST['fechaFin'], "%Y-%m-%d").date()
    patrimonio = Patrimonio.objects.get(pk=int(request.POST['patrimonio']))
    proyecto = ProyectoConservacion.objects.get(pk=pk)
    actividad = Actividad.objects.create(
        codigo=codigo,
        nombre=nombre,
        descripcion=descripcion,
        fechaInicio=fechaInicio,
        fechaFin=fechaFin,
        presupuesto=0.00,
        gastoTotal=0.00,
        proyecto=proyecto,
        patrimonio=patrimonio)
    proyecto.cantidadAct = Actividad.objects.filter(proyecto=proyecto).filter(estado='1').count()
    proyecto.save()
    # print()
    # fechaInicio = datetime.date.today()
    # fechaFin = datetime.date.today()
    # tipo = int((request.POST['tipoPlan']))
    # project = ProyectoConservacion.objects.create(
    #     codigo = codigo,
    #     nombre=nombre,
    #     tipoProyecto=tipo,
    #     fechaInicio=fechaInicio,
    #     fechaFin=fechaFin)
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)

@api_view(('POST',))
def addTask(request, pk):
    codigo = "ACT00"
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    presupuesto = request.POST['presupuesto']
    gasto = request.POST['gasto']
    fechaRegistro = datetime.datetime.strptime(request.POST['fechaRegistro'], "%Y-%m-%d").date()
    fecha = datetime.datetime.strptime(request.POST['fecha'], "%Y-%m-%d").date()
    actividad = Actividad.objects.get(pk=pk)
    tarea = ProyectoConservacion.objects.create(
        codigo=codigo,
        nombre=nombre,
        descripcion=descripcion,
        presupuesto=presupuesto,
        gasto=gasto,
        fechaRegistro=fechaRegistro,
        fecha=fecha,
        actividad=actividad)
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)