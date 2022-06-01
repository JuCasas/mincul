import datetime

from django.shortcuts import render, redirect

from authentication.models import User
from traslado.models import SolicitudTraslado, EntidadSolicitante

from django.core import serializers
from django.http import JsonResponse

def addTransfer(request):
    if request.POST:
        print(request.POST)
        solicitudTraslado = SolicitudTraslado.objects.create(entidadSolicitante_id=request.POST['nombreInstitucion'],
                                                    nombreExposicion=request.POST['nombreExposicion'],
                                                    pais=request.POST['pais'],
                                                    ubigeoDestino=request.POST['ubigeo'],
                                                    gestorConservacionTraslados_id=request.POST['comisario'],
                                                    gestorPatrimonio_id=request.POST['comisario'],
                                                    fechaSalidaProgramada=request.POST['fechaSalidaProgramada'],
                                                    fechaRetornoProgramada=request.POST['fechaRetornoProgramada'],
                                                    numeroResolucion=request.POST['nResolucion']
                                                    )
        return redirect('listTransfer')
    else:
        entidades = EntidadSolicitante.objects.filter()
        comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

        context = {
            'entidades': entidades,
            'comisarios':comisarios
        }
        return render(request,'traslado/transfer_add.html',context)
    
    
def listEntidades(request):

    entidades = EntidadSolicitante.objects.filter()
    context = {
        'entidades': entidades
    }
    
    return render(request, 'traslado/list_entidades.html',context=context)


def registrarSolicitante(request):
    message_error="Entidad Agregada"
    doiSolicitante = request.POST["doiSolicitante"]
    nombreSolicitante  = request.POST["nombreSolicitante"]
    correo = request.POST["correo"]
    direccion = request.POST["direccion"]
    pais = request.POST["pais"]
    telefono = request.POST["telefono"]

    registro = EntidadSolicitante.objects.filter(doiSolicitante=doiSolicitante)
    if (registro.__len__() == 0):
        EntidadSolicitante.objects.create(doiSolicitante=doiSolicitante,
                                          nombreSolicitante=nombreSolicitante,
                                          correo=correo,
                                          direccion=direccion,
                                          pais=pais,
                                          telefono=telefono)
    else:
        message_error = "La Entidad ya se encuentra registrado"
    return JsonResponse({"message_error": message_error}, status=200)
    
def listarSolicitantes(request):
    # patrimoniopk = request.POST["patrimoniopk"]    
    # registros = SolicitudTraslado.objects.filter(patrimonios_id=patrimoniopk)
    solicitantes = SolicitudTraslado.objects.all()
    # for item in registros:
    #     solicitantes.append(item.entidadSolicitante)
    sol_instance = serializers.serialize('json', solicitantes)
    return JsonResponse({"asistentes": sol_instance}, status=200)


def eliminarSolicitantes(request, id):
    entidad = EntidadSolicitante.objects.get(id=id)
    print(entidad)
    entidad.delete()
    return redirect('/traslado/entidades')

    # solicitantepk = request.POST['solicitantepk']
    # solicitante = EntidadSolicitante.objects.get(pk=solicitantepk)
    #
    # solicitante.delete()
    # return JsonResponse({}, status=200)

def eliminarEntidad(request,id):
    entidad = EntidadSolicitante.objects.get(id=id)
    entidad.delete()

    return redirect('/traslado/entidades')