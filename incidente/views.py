from django.shortcuts import render

# Create your views here.
from incidente.models import Incidente
from patrimonios.models import Patrimonio, Institucion
from django.http import HttpResponseRedirect
from django.urls import reverse

class Incidentado:
    @classmethod
    def fromPatrimonio(inc, patrimonio):
        inc.nombre = patrimonio.nombreTituloDemoninacion
        inc.documentos = patrimonio.documentos
        inc.lat = patrimonio.lat
        inc.long = patrimonio.long

    @classmethod
    def fromInstitucion(inc, institucion):
        inc.nombre = institucion.nombre
        inc.documentos = institucion.documentos
        inc.lat = institucion.lat
        inc.long = institucion.long

def patrimonio_incidente_listar(request):

    patrimonios = Patrimonio.objects.filter(tipoPatrimonio=2, institucion=None, estado=1)
    instituciones = Institucion.objects.filter(estado=1)

    incPat = [Incidentado.fromPatrimonio(p) for p in patrimonios]
    incIns = [Incidentado.fromInstitucion(i) for i in instituciones]

    incidentados = []
    incidentados.append(incPat)
    incidentados.append(incIns)

    context = {
        'patrimonios': Patrimonio.objects.all(),
        'incidentes': Incidente.objects.all(),
        'incidentados': incidentados
    }

    return render(request, 'incidencia/patrimonio_incidente_listar.html', context=context)


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