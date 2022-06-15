import datetime

from django.shortcuts import render, redirect

from authentication.models import User
from mincul.settings import MEDIA_URL
from mincul_app.models import Documento
from patrimonios.models import Patrimonio
from traslado.models import SolicitudTraslado, EntidadSolicitante, DocumentoPorSolicitud
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core import serializers
from django.http import JsonResponse

def addTransfer(request):
    if request.POST:
        solicitudTraslado = SolicitudTraslado.objects.create(entidadSolicitante_id=request.POST['nombreInstitucion'],
                                                             destino=request.POST['destino'],
                                                             nombreExposicion=request.POST['nombreExposicion'],
                                                             pais=request.POST['pais'],
                                                             gestorConservacionTraslados_id=request.POST['comisario'],
                                                             gestorPatrimonio_id=request.POST['comisario'],
                                                             fechaSalidaProgramada=request.POST[
                                                                 'fechaSalidaProgramada'],
                                                             fechaRetornoProgramada=request.POST[
                                                                 'fechaRetornoProgramada'],
                                                             numeroResolucion=request.POST['nResolucion']
                                                             )
        if request.POST['lista']:
            patrimoniosSolicitados = list(request.POST['lista'].split(","))
            for idPatrimonio in patrimoniosSolicitados:
                solicitudTraslado.patrimonios.add(Patrimonio.objects.get(pk=idPatrimonio))

        for f in request.FILES.getlist('file'):
            doc = Documento.objects.create(url=f)
            DocumentoPorSolicitud.objects.create(documento_id=doc.pk, solicitud_id=solicitudTraslado.pk)

        return redirect('list_transfers')
    else:
        entidades = EntidadSolicitante.objects.filter()
        comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")
        patrimonios = Patrimonio.objects.filter()

        context = {
            'entidades': entidades,
            'comisarios': comisarios,
        }
        return render(request, 'traslado/transfer_add.html', context)

def listarPatrimoniosTraslado(request):
    filtro = request.GET['q']
    patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=filtro)
    ser_instance = serializers.serialize('json', list(patrimonios),
                                         fields=('id', 'nombreTituloDemoninacion','categoria', 'tipoPatrimonio'))
    print(ser_instance)
    return JsonResponse({"patrimoniosAjax": ser_instance}, status=200)

def entidadEmail(request):
    print('***********************************************************************************************************')
    print(request.POST['entidad'])
    print('***********************************************************************************************************')
    entidad = EntidadSolicitante.objects.get(pk=request.POST['entidad']).correo
    return JsonResponse({"email": entidad}, status=200)

def validarResolucion(request):
    existe = SolicitudTraslado.objects.filter(numeroResolucion=request.POST['nResolucion']).exists()
    print(existe)
    return JsonResponse({"existe": existe}, status=200)

def listTranfers(request):

    traslados = SolicitudTraslado.objects.all()
    context = {
        'traslados': traslados
    }

    return render(request,'traslado/transfer_list.html', context)


def viewTranfer(request,pk):
    media_path = MEDIA_URL
    traslado = SolicitudTraslado.objects.get(pk=pk)
    entidades = EntidadSolicitante.objects.filter()
    comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

    #Nota, se debe considerar los patrominos del traslado
    patrimonios = traslado.patrimonios.all()
    documentos =  DocumentoPorSolicitud.objects.filter(solicitud_id=traslado.pk)

    context = {
        'traslado': traslado,
        'entidades': entidades,
        'comisarios': comisarios,
        'patrimonios': patrimonios,
        'documentos': documentos,
        'media_path': media_path
    }

    return render(request,'traslado/transfer_view.html', context)



def editTransfer(request,pk):
    media_path = MEDIA_URL
    traslado = SolicitudTraslado.objects.get(pk=pk)
    entidades = EntidadSolicitante.objects.filter()
    comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

    #Nota, se debe considerar los patrominos del traslado
    patrimonios = traslado.patrimonios.all()
    documentos = DocumentoPorSolicitud.objects.filter(solicitud_id=traslado.pk)
    estadosEditables = [('2', 'Evaluar'),('3', 'Rechazar'),('4', 'Aprobadar')]



    context = {
        'traslado': traslado,
        'entidades': entidades,
        'comisarios': comisarios,
        'patrimonios': patrimonios,
        'documentos': documentos,
        'media_path': media_path,
        'estadosEditables': estadosEditables
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



def actualizarEstado(request):

    estado = request.POST.get('nuevo_estado')
    detalle_rechazo = request.POST.get('detalle_rechazo')

    trasladopk = request.POST.get('traslado_pk')
    traslado = SolicitudTraslado.objects.get(pk=trasladopk)

    traslado.estado = estado
    mensaje = ''

    asunto=''
    if(estado=='3'):
        asunto = 'Aprobación de solicitud de traslado '+ traslado.numeroResolucion
        traslado.detalleRechazo = detalle_rechazo
        mensaje = 'Su solicitud de traslado ha sido rechazada de debido al siguiente motivo: '+ detalle_rechazo
    elif(estado=='4'):
        asunto = 'Desaprobación de solicitud de traslado ' + traslado.numeroResolucion
        mensaje = 'Su solicitud de traslado ha sido aceptada de manera satisfactoria'

    traslado.save()

    correo = traslado.entidadSolicitante.correo
    asunto: "Estado de solicitud"

    if(estado=='3' or estado=='4'):
        send_form_email(asunto, correo, mensaje)

    return JsonResponse({}, status=200)


def send_form_email(subject, recipient, texto):
    sender = 'info@inova.team'
    context = {
        'texto': texto,
        'correo_entidad': recipient,
    }
    template = get_template('traslado/body_email_transfer.html')
    content = template.render(context)
    correo = recipient.strip()
    email = EmailMultiAlternatives(subject, '', sender, [correo], cc=[])
    email.attach_alternative(content, 'text/html')
    # email.send()
    print('Se envió correo')
