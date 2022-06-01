import datetime

from django.shortcuts import render, redirect

from authentication.models import User
from patrimonios.models import Patrimonio
from traslado.models import SolicitudTraslado, EntidadSolicitante

from django.core import serializers
from django.http import JsonResponse

def addTransfer(request):
    if request.POST:
        print(request.POST)
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
    print("//////////////////////////////////////////////////////////")
    patrimonios = Patrimonio.objects.filter()
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
    patrimonios = {}

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
