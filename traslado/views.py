import datetime

from django.shortcuts import render, redirect

from authentication.models import User
from traslado.models import SolicitudTraslado, EntidadSolicitante


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