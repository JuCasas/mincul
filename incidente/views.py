from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view

from incidente.models import Incidente
from incidente.serializers import IncidenteSerializer
from patrimonios.models import Patrimonio, Institucion, PuntoGeografico
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response


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
def patrimonio_incidente_listar(request):
    if request.is_ajax():
        incident = query_incidents_by_args(**request.GET)
        for inc in incident['items']:
          print(inc.zona.nombre)
        serializer = IncidenteSerializer((incident['items']),many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = incident['total']
        result['recordsFiltered'] = incident['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
        return render(request, 'incidencia/patrimonio_incidente_listar.html')


def incidente_reporte_listar(request, patrimonio_pk):

    context = {
        'incidentes': Incidente.objects.filter(patrimonio_id=patrimonio_pk),
        'patrimonio_pk': patrimonio_pk
    }

    return render(request, 'incidencia/incidente_reporte_listar.html', context=context)

def incidente_reporte_agregar(request, patrimonio_pk):

    if request.POST:
        print(request.POST)
        incidente = Incidente.objects.create()
        incidente.detalle = request.POST.get("detalle")
        incidente.fechaRegistro = request.POST.get("fecha_reporte")
        incidente.descripcion = request.POST.get("descripcion")
        incidente.patrimonio_id = patrimonio_pk
        incidente.save()
        return HttpResponseRedirect(reverse(incidente_reporte_listar, kwargs={'patrimonio_pk':patrimonio_pk}))

    return render(request, 'incidencia/incidente_reporte_agregar.html')

def incidente_reporte_modificar(request, patrimonio_pk, incidente_pk):

    context = {
        'incidente': Incidente.objects.get(id=incidente_pk)
    }

    if request.POST:
        incidente = Incidente.objects.get(pk=incidente_pk)
        incidente.detalle = request.POST.get("detalle")
        incidente.fechaRegistro = request.POST.get("fecha_reporte")
        incidente.descripcion = request.POST.get("descripcion")
        incidente.patrimonio_id = patrimonio_pk
        incidente.save()
        return HttpResponseRedirect(reverse(incidente_reporte, kwargs={'patrimonio_pk':patrimonio_pk, 'incidente_pk':incidente_pk}))

    return render(request, 'incidencia/incidente_reporte_modificar.html', context)


def incidente_reporte(request, patrimonio_pk, incidente_pk):

    context = {
        'incidente': Incidente.objects.get(id=incidente_pk)
    }

    return render(request, 'incidencia/incidente_reporte.html', context=context)