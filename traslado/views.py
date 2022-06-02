import datetime

from django.shortcuts import render, redirect

from authentication.models import User
from patrimonios.models import Patrimonio
from traslado.models import SolicitudTraslado, EntidadSolicitante

from django.core import serializers
from django.http import JsonResponse

def addTransfer(request):
    if request.POST:
        patrimoniosSolicitados = list(request.POST['lista'].split(","))
        solicitudTraslado = SolicitudTraslado.objects.create(entidadSolicitante_id=request.POST['nombreInstitucion'],
                                                             nombreExposicion=request.POST['nombreExposicion'],
                                                             pais=request.POST['pais'],
                                                             ubigeoDestino=request.POST['ubigeo'],
                                                             gestorConservacionTraslados_id=request.POST['comisario'],
                                                             gestorPatrimonio_id=request.POST['comisario'],
                                                             fechaSalidaProgramada=request.POST[
                                                                 'fechaSalidaProgramada'],
                                                             fechaRetornoProgramada=request.POST[
                                                                 'fechaRetornoProgramada'],
                                                             numeroResolucion=request.POST['nResolucion']
                                                             )
        for idPatrimonio in patrimoniosSolicitados:
            solicitudTraslado.patrimonios.add(Patrimonio.objects.get(pk=idPatrimonio))

        return redirect('list_transfers')
    else:
        entidades = EntidadSolicitante.objects.filter()
        comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")
        patrimonios = Patrimonio.objects.filter()

        context = {
            'entidades': entidades,
            'comisarios': comisarios,
            'patrimonios': patrimonios,
        }
        return render(request, 'traslado/transfer_add.html', context)

def listarPatrimoniosTraslado(request):
    filtro = request.GET['q']
    patrimonios = Patrimonio.objects.filter(tituloDemoninacion__icontains=filtro)
    ser_instance = serializers.serialize('json', list(patrimonios),
                                         fields=('id', 'tituloDemoninacion','categoria', 'tipoPatrimonio'))
    print(ser_instance)
    return JsonResponse({"patrimoniosAjax": ser_instance}, status=200)

def listTranfers(request):

    traslados = SolicitudTraslado.objects.all()
    context = {
        'traslados': traslados
    }

    return render(request,'traslado/transfer_list.html', context)


def viewTranfer(request,pk):

    traslado = SolicitudTraslado.objects.get(pk=pk)
    entidades = EntidadSolicitante.objects.filter()
    comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

    #Nota, se debe considerar los patrominos del traslado
    patrimonios = traslado.patrimonios.all()
    for patrimonio in patrimonios:
        print(patrimonio.tituloDemoninacion)

    context = {
        'traslado': traslado,
        'entidades': entidades,
        'comisarios': comisarios,
        'patrimonios': patrimonios
    }

    return render(request,'traslado/transfer_view.html', context)



def editTransfer(request,pk):

    traslado = SolicitudTraslado.objects.get(pk=pk)
    entidades = EntidadSolicitante.objects.filter()
    comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

    #Nota, se debe considerar los patrominos del traslado
    patrimonios = {}

    context = {
        'traslado': traslado,
        'entidades': entidades,
        'comisarios': comisarios,
        'patrimonios': patrimonios
    }

    return render(request,'traslado/transfer_edit.html', context)


def listEntidades(request):
    entidades = EntidadSolicitante.objects.filter()
    context = {
        'entidades': entidades
    }

    return render(request, 'traslado/list_entidades.html', context=context)

def eliminarSolicitantes(request, id):
    entidad = EntidadSolicitante.objects.get(id=id)
    # print(entidad)
    entidad.delete()
    return redirect('/traslado/entidades')

def registrarSolicitantes(request):

    doiSolicitante = request.POST['inputDOI']
    nombreSolicitante = request.POST['inputNombre']
    correo = request.POST['inputCorreo']
    direccion = request.POST['inputDireccion']
    pais = request.POST['inputPais']
    telefono = request.POST['inputTelefono']

    solicitante = EntidadSolicitante.objects.create(doiSolicitante=doiSolicitante,nombreSolicitante=nombreSolicitante,correo=correo,direccion=direccion,pais=pais,telefono=telefono)

    return redirect('/traslado/entidades')

def editarSolicitante(request):

    id = request.POST['inputID']
    doiSolicitante = request.POST['inputDOI2']
    nombreSolicitante = request.POST['inputNombre2']
    correo = request.POST['inputCorreo2']
    direccion = request.POST['inputDireccion2']
    pais = request.POST['inputPais2']
    telefono = request.POST['inputTelefono2']

    solicitante = EntidadSolicitante.objects.get(id=id)

    solicitante.doiSolicitante = doiSolicitante
    solicitante.nombreSolicitante = nombreSolicitante
    solicitante.correo = correo
    solicitante.direccion = direccion
    solicitante.pais = pais
    solicitante.telefono = telefono
    solicitante.save()

    return redirect('/traslado/entidades')

def eliminacionSolicitante(request):
    doi = request.POST['inputDOI3']
    entidad = EntidadSolicitante.objects.get(doiSolicitante=doi)
    entidad.delete()
    return redirect('/traslado/entidades')