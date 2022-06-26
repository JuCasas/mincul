import datetime

from django.db.models import Count
from django.http import JsonResponse
from django.core import serializers
from authentication.models import User
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from conservacion.models import ProyectoConservacion, Actividad, Tarea, Campo
from conservacion.serializers import ProyectoConservacionSerializer, ActividadSerializer, TareaSerializer, \
    PatrimonioSerializer, ConservadorSerializer
from mincul.settings import MEDIA_URL
from mincul_app.models import Documento
from patrimonios.models import Patrimonio, Institucion, PuntoGeografico
from incidente.models import Incidente
from incidente.serializers import IncidenteSerializer, PuntoGeograficoSerializer


def query_projects_by_args(**kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]
    type_filter = kwargs.get('type_filter', None)[0]
    status_filter = kwargs.get('status_filter', None)[0]
    patrimony_filter = kwargs.get('patrimony_filter', None)[0]
    order_column = kwargs.get('order_column', None)[0]
    order = kwargs.get('order', None)[0]
    if (len(patrimony_filter) == 0):
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
    search_value = kwargs.get('search_value', None)[0]
    patrimonio_filter = kwargs.get('patrimonio_filter', None)[0]
    status_filter = kwargs.get('status_filter', None)[0]
    order_column = kwargs.get('order_column', None)[0]
    order = kwargs.get('order', None)[0]

    project = ProyectoConservacion.objects.get(pk=pk)
    queryset = Actividad.objects.annotate(conservadores_count=Count('conservadores')).filter(proyecto=project).filter(estado='1')

    total = queryset.count()

    order_column = Actividad.ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column

    if search_value:
        queryset = queryset.filter(nombre__icontains=search_value)
    if patrimonio_filter:
        patrimonio = Patrimonio.objects.get(pk=patrimonio_filter)
        queryset = queryset.filter(patrimonio =patrimonio)
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
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
    queryset = Tarea.objects.filter(actividad=activity).filter()

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


def query_incidents_by_args(**kwargs):
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]
    type_filter = kwargs.get('type_filter', None)[0]
    status_filter = kwargs.get('status_filter', None)[0]
    zone_filter = kwargs.get('zone_filter', None)[0]
    order_column = kwargs.get('order_column', None)[0]
    order = kwargs.get('order', None)[0]
    if (len(zone_filter) == 0):
        queryset = Incidente.objects.filter(estado='1')
    else:
        zona = PuntoGeografico.objects.get(pk=int(zone_filter))
        queryset = Incidente.objects.filter(zona=zona)

    total = queryset.count()

    # order_column = ProyectoConservacion.ORDER_COLUMN_CHOICES[order_column]
    # if order == 'desc':
    #   order_column = '-' + order_column

    if search_value:
        queryset = queryset.filter(codigo__icontains=search_value)
    if type_filter:
        queryset = queryset.filter(tipoAfectacion=type_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)

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
    start = (page - 1) * length
    end = start + length
    queryset = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=search).order_by(
        'nombreTituloDemoninacion')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = PatrimonioSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def addConservador(request):
    queryset = User.objects.all()
    count = queryset.count()
    serializer = ConservadorSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def addRelacion(request, pk):
    proyecto = ProyectoConservacion.objects.get(pk=pk)
    queryset = Actividad.objects.filter(proyecto=proyecto).filter(estado='1')
    count = queryset.count()
    serializer = ActividadSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def listProjects(request, **kwargs):
    if request.is_ajax():
        project = query_projects_by_args(**request.GET)
        serializer = ProyectoConservacionSerializer((project['items']), many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = project['total']
        result['recordsFiltered'] = project['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
        context = {
            'status_choices': ProyectoConservacion.STATUS,
            'typeProjects': ProyectoConservacion.TIPOS
        }
        return render(request, 'proyectoConservacion/project_list.html', context)


@api_view(('POST',))
def addProject(request):
    try:
        nombre = request.POST['nombre']
        fechaInicio = datetime.date.today()
        fechaFin = datetime.date.today()
        tipo = int((request.POST['tipoPlan']))
        project = ProyectoConservacion.objects.create(
            nombre=nombre,
            tipoProyecto=tipo,
            fechaInicio=fechaInicio,
            fechaFin=fechaFin)
        project.codigo = "PROY" + str(project.id).zfill(6)
        project.save()
        return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        result = dict()
        result['success'] = False
        result['message'] = str(e)  # or custom message
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def editProject(request, pk):
    try:
        project = ProyectoConservacion.objects.get(pk=pk)
        nombre = request.POST['nombre']
        tipo = int((request.POST['tipoPlan']))
        project.nombre = nombre
        project.tipoProyecto = tipo
        project.save()
        return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        result = dict()
        result['success'] = False
        result['message'] = str(e)  # or custom message
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def deleteProject(request, pk):
    project = ProyectoConservacion.objects.get(pk=pk)
    project.estado = '2'
    project.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def deletePatrimony(request, pk):
    project = ProyectoConservacion.objects.get(pk=pk)
    patrimonio = Patrimonio.objects.get(pk=int(request.POST['patrimonio']))
    project.patrimonios.remove(patrimonio)
    project.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def listActivities(request, pk):
    if request.is_ajax():
        activity = query_activities_by_args(pk, **request.GET)
        serializer = ActividadSerializer((activity['items']), many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = activity['total']
        result['recordsFiltered'] = activity['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
        proyecto = ProyectoConservacion.objects.get(pk=pk)
        patrimonios = proyecto.patrimonios.all()
        media_path = MEDIA_URL

        context = {
            'media_path': media_path,
            'status_choices': Actividad.STATUS,
            'project': proyecto,
            'patrimonios': patrimonios
        }
        return render(request, 'proyectoConservacion/activity_list.html', context)


@api_view(('GET',))
def listIncidents(request, pk):
    if request.is_ajax():
        incident = query_incidents_by_args(**request.GET)
        for inc in incident['items']:
            print(inc.zona.nombre)
        serializer = IncidenteSerializer((incident['items']), many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = incident['total']
        result['recordsFiltered'] = incident['count']
        print(type(result))
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
        context = {
            'project': ProyectoConservacion.objects.get(pk=pk),
            'status_choices': Incidente.STATUS,
            'typeIncidents': Incidente.AFECTACION
        }
        return render(request, 'proyectoConservacion/incident_list.html', context)


@api_view(('GET',))
def listPatrimonys(request, pk):
    context = {
        'project': ProyectoConservacion.objects.get(pk=pk),
    }
    return render(request, 'proyectoConservacion/patrimonys_list.html', context)


@api_view(('GET',))
def listPatrimonysForProject(request, pk):
    project = ProyectoConservacion.objects.get(pk=pk)
    search = request.GET['search_value']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    queryset = project.patrimonios.all()
    if search:
        queryset = queryset.filter(nombreTituloDemoninacion__icontains=search).order_by('nombreTituloDemoninacion')
    count = queryset.count()
    queryset = queryset[start:start + length]
    serializer = PatrimonioSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def addPatrimony(request, pk):
    patrimonio = Patrimonio.objects.get(pk=int(request.POST['patrimonio']))
    proyecto = ProyectoConservacion.objects.get(pk=pk)
    proyecto.patrimonios.add(patrimonio)
    proyecto.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def listTasks(request, pk):
    if request.is_ajax():
        task = query_tasks_by_args(pk, **request.GET)
        serializer = TareaSerializer((task['items']), many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = task['total']
        result['recordsFiltered'] = task['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
        context = {
            'activity': Actividad.objects.get(pk=pk),
            'project': Actividad.objects.get(pk=pk).proyecto
        }
        return render(request, 'proyectoConservacion/task_list.html', context)


@api_view(('POST',))
def addActivity(request, pk):
    try:
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        fechaInicio = datetime.datetime.strptime(request.POST['fechaInicio'], "%Y-%m-%d").date()
        fechaFin = datetime.datetime.strptime(request.POST['fechaFin'], "%Y-%m-%d").date()
        patrimonio = Patrimonio.objects.get(pk=int(request.POST['patrimonio']))
        proyecto = ProyectoConservacion.objects.get(pk=pk)
        actividad = Actividad.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fechaInicio=fechaInicio,
            fechaFin=fechaFin,
            presupuesto=0.00,
            gastoTotal=0.00,
            proyecto=proyecto,
            patrimonio=patrimonio)

        if request.POST['conservadoresLista']:
            conservadores = list(request.POST['conservadoresLista'].split(","))
            for idConservador in conservadores:
                actividad.conservadores.add(User.objects.get(pk=idConservador))

        if request.POST['relacionesLista']:
            relaciones = list(request.POST['relacionesLista'].split(","))
            for idRelacion in relaciones:
                actividad.relaciones.add(Actividad.objects.get(pk=idRelacion))

        for f in request.FILES.getlist('file'):
            doc = Documento.objects.create(url=f)
            actividad.documentos.add(doc)

        actividad.codigo = "ACT" + str(actividad.id).zfill(5)
        actividad.save()
        proyecto.cantidadAct = Actividad.objects.filter(proyecto=proyecto).filter(estado='1').count()
        proyecto.save()
        return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        result = dict()
        result['success'] = False
        result['message'] = str(e)  # or custom message
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def editActivity(request, pk, pkActividad):
    try:
        print("######")
        print(request.POST)
        print(request.FILES)
        actividad = Actividad.objects.get(pk=pkActividad)
        actividad.nombre = request.POST['nombre']
        actividad.descripcion = request.POST['descripcion']
        actividad.fechaInicio = datetime.datetime.strptime(request.POST['fechaInicio'], "%Y-%m-%d").date()
        actividad.fechaFin = datetime.datetime.strptime(request.POST['fechaFin'], "%Y-%m-%d").date()
        actividad.patrimonio = Patrimonio.objects.get(pk=int(request.POST['patrimonio']))

        actividad.conservadores.clear()
        if request.POST['conservadoresLista']:
            conservadores = list(request.POST['conservadoresLista'].split(","))
            for idConservador in conservadores:
                actividad.conservadores.add(User.objects.get(pk=idConservador))

        actividad.relaciones.clear()
        if request.POST['relacionesLista']:
            relaciones = list(request.POST['relacionesLista'].split(","))
            for idRelacion in relaciones:
                actividad.relaciones.add(Actividad.objects.get(pk=idRelacion))

        for f in request.FILES.getlist('file'):
            doc = Documento.objects.create(url=f)
            actividad.documentos.add(doc)

        actividad.save()
        return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        result = dict()
        result['success'] = False
        result['message'] = str(e)  # or custom message
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def deleteActivity(request, pk, pkActividad):
    actividad = Actividad.objects.get(pk=pkActividad)
    actividad.estado = '2'
    actividad.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def addTaskView(request, pk):
    actividad = Actividad.objects.get(pk=pk)
    conservadores = actividad.conservadores.all()

    context = {
        'activity': actividad,
        'conservadores': conservadores
    }
    return render(request, 'proyectoConservacion/addTask_view.html', context)


@api_view(('POST',))
def addTask(request, pk):
    print('Request:', request.POST)

    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    responsablepk = request.POST['conservador']
    responsable = User.objects.get(pk=responsablepk)
    presupuesto = request.POST['presupuesto']
    fechaRegistro = datetime.datetime.strptime(request.POST['fechaRegistro'], "%Y-%m-%d").date()
    fecha = datetime.datetime.strptime(request.POST['fecha'], "%Y-%m-%d").date()
    actividad = Actividad.objects.get(pk=pk)
    tarea = Tarea.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        responsable=responsable,
        presupuesto=float(presupuesto),
        gasto=0.00,
        fechaRegistro=fechaRegistro,
        fecha=fecha,
        actividad=actividad)
    tarea.codigo = "A" + str(tarea.id).zfill(3)
    tarea.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('POST',))
def editTask(request, pk):
    tarea = Tarea.objects.get(pk=pk)
    tarea.nombre = request.POST['nombre']
    tarea.descripcion = request.POST['descripcion']
    tarea.presupuesto = request.POST['presupuesto']
    tarea.fechaRegistro = datetime.datetime.strptime(request.POST['fechaRegistro'], "%Y-%m-%d").date()
    tarea.fecha = datetime.datetime.strptime(request.POST['fecha'], "%Y-%m-%d").date()
    tarea.estado = request.POST['estado']
    tarea.save()
    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


@api_view(('GET',))
def editTaskView(request, pk):
    tarea = Tarea.objects.get(pk=pk)
    secciones = Campo.objects.filter(tarea_id=tarea.pk)
    context = {
        'task': tarea,
        'secciones': secciones,
        'activity': Actividad.objects.get(pk=Tarea.objects.get(pk=pk).actividad.pk)
    }
    return render(request, 'proyectoConservacion/editTask_view.html', context)


@api_view(('GET',))
def detailTaskView(request, pk):
    context = {
        'task': Tarea.objects.get(pk=pk),
        'activity': Actividad.objects.get(pk=Tarea.objects.get(pk=pk).actividad.pk)
    }
    return render(request, 'proyectoConservacion/detailTask_view.html', context)


def updateTaskState(request):
    task_pk = request.POST.get('task_pk')
    task = Tarea.objects.get(pk=task_pk)
    nuevo_estado = ''

    if (task.estado == '1'):
        nuevo_estado = '2'
    elif (task.estado == '2'):
        nuevo_estado = '3'

    task.estado = nuevo_estado
    task.save()
    return JsonResponse({}, status=200)


@api_view(('POST',))
def addSection(request, pk):
    print('Dentro de agregar sección>>>>>>>>')
    print(request.POST)

    tarea = Tarea.objects.get(pk=pk)
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']

    evidencias = request.FILES

    campo = Campo.objects.create(nombre=nombre, contenido=descripcion, tarea=tarea)
    campo.save()

    n_files = len(evidencias)

    for i in range(n_files):
        name = 'files'+str(i)
        documento = Documento.objects.create(url=request.FILES.get(name))
        campo.documentos.add(documento)

    campo.save()

    return Response({}, status=status.HTTP_200_OK, template_name=None, content_type=None)


def listSections(request, pk):
    secciones = Campo.objects.filter(tarea_id=pk)
    ser_instance = serializers.serialize('json', secciones)
    return JsonResponse({"secciones": ser_instance}, status=200)
