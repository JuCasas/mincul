from html import entities
from django.shortcuts import render

# Create your views here.
from patrimonios.models import Patrimonio
from django.core import serializers
from django.http import JsonResponse

from traslado.models import EntidadSolicitante, SolicitudTraslado

def patrimonio_list(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'patrimonio/patrimony_list.html', context=context)

def patrimonio_gestor(request):
    
    return render(request, 'patrimonio/patrimony_gestor.html')


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


def eliminarSolicitantes(request):
    solicitantepk = request.POST['solicitantepk']
    solicitante = EntidadSolicitante.objects.get(pk=solicitantepk)
   
    solicitante.delete()
    return JsonResponse({}, status=200)