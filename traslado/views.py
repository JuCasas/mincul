import datetime
import os

from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import User
from traslado.serializers import TrasladoSerializer
from mincul.settings import MEDIA_URL
from mincul_app.models import Documento
from patrimonios.models import Patrimonio
from traslado.models import SolicitudTraslado, EntidadSolicitante, DocumentoPorSolicitud
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core import serializers
from django.http import JsonResponse


def query_transfer_by_args(**kwargs):
    print(kwargs)
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]
    status_filter = kwargs.get('status_filter', None)[0]
    order_column = kwargs.get('order_column', None)[0]
    order = kwargs.get('order', None)[0]

    queryset = SolicitudTraslado.objects.all()

    total = queryset.count()

    # order_column = SolicitudTraslado.ORDER_COLUMN_CHOICES[order_column]
    # if order == 'desc':
    #   order_column = '-' + order_column

    if search_value:
        queryset = queryset.filter(entidadSolicitante__nombreSolicitante__icontains=search_value)
    if status_filter:
        queryset = queryset.filter(estado=status_filter)

    count = queryset.count()
    # queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }


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
                                                             # fechaRetornoProgramada=request.POST[
                                                             #     'fechaRetornoProgramada'],
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
        operacion = "agregar"
        idEditar = 0

        context = {
            'entidades': entidades,
            'comisarios': comisarios,
            'operacion': operacion,
            'idEditar': idEditar
        }
        return render(request, 'traslado/transfer_add.html', context)


def listarPatrimoniosTraslado(request):
    filtro = request.GET['q']
    patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=filtro)
    ser_instance = serializers.serialize('json', list(patrimonios),
                                         fields=('id', 'nombreTituloDemoninacion', 'categoria', 'tipoPatrimonio'))
    print(ser_instance)
    return JsonResponse({"patrimoniosAjax": ser_instance}, status=200)


def entidadEmail(request):
    print('***********************************************************************************************************')
    print(request.POST['entidad'])
    print('***********************************************************************************************************')
    entidad = EntidadSolicitante.objects.get(pk=request.POST['entidad']).correo
    return JsonResponse({"email": entidad}, status=200)


def validarResolucion(request):
    print(request.POST)
    print("porblmea probnlema problema")
    pk = request.POST['idEditar']
    print(pk)
    if (pk == '0'):
        existe = SolicitudTraslado.objects.filter(numeroResolucion=request.POST['nResolucion']).exists()
    else:
        nResActual = SolicitudTraslado.objects.get(pk=pk).numeroResolucion
        print(nResActual)
        existe = SolicitudTraslado.objects.filter(numeroResolucion=request.POST['nResolucion']).exclude(
            numeroResolucion=nResActual).exists()
    print(existe)
    return JsonResponse({"existe": existe}, status=200)

def eliminarDocumentoTraslado(request):
    traslado = SolicitudTraslado.objects.get(pk=request.POST['traslado'])
    documento = Documento.objects.get(pk=request.POST['documento'])
    path = documento.url.path
    os.remove(path)
    documento.delete()
    traslado.save()
    return JsonResponse({}, status=200)


def validarDOI(request):
    doiEntrante = request.POST['DOI']
    edit = request.POST['EDIT']
    pkEditar = request.POST['PKEDITAR']
    if (edit == '0'):
        existe = EntidadSolicitante.objects.filter(doiSolicitante=request.POST['DOI']).exists()
    else:
        print("EDITAR")
        doiSolicitanteActual = EntidadSolicitante.objects.get(pk=pkEditar).doiSolicitante
        existe = EntidadSolicitante.objects.filter(doiSolicitante=request.POST['DOI']).exclude(
            doiSolicitante=doiSolicitanteActual).exists()
    if existe:
        return JsonResponse(False, status=200, safe=False)
    else:
        return JsonResponse(True, status=200, safe=False)


@api_view(('GET',))
def listTranfers(request):
    if request.is_ajax():
        tranfers = query_transfer_by_args(**request.GET)
        serializer = TrasladoSerializer((tranfers['items']), many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = tranfers['total']
        result['recordsFiltered'] = tranfers['count']

        print("####################################")
        print(result)
        print("####################################")
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
        traslados = SolicitudTraslado.objects.all()
        context = {
            'traslados': traslados
        }

    return render(request, 'traslado/transfer_list.html', context)


def viewTranfer(request, pk):
    media_path = MEDIA_URL
    traslado = SolicitudTraslado.objects.get(pk=pk)
    entidades = EntidadSolicitante.objects.filter()
    comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

    # Nota, se debe considerar los patrominos del traslado
    patrimonios = traslado.patrimonios.all()
    documentos = DocumentoPorSolicitud.objects.filter(solicitud_id=traslado.pk)

    context = {
        'traslado': traslado,
        'entidades': entidades,
        'comisarios': comisarios,
        'patrimonios': patrimonios,
        'documentos': documentos,
        'media_path': media_path
    }

    return render(request, 'traslado/transfer_view.html', context)


def editTransfer(request, pk):
    if request.POST:
        solicitudTraslado = SolicitudTraslado.objects.get(pk=pk)
        solicitudTraslado.entidadSolicitante_id = request.POST['nombreInstitucion']
        solicitudTraslado.destino = request.POST['destino']
        solicitudTraslado.nombreExposicion = request.POST['nombreExposicion']
        solicitudTraslado.pais = request.POST['pais']
        solicitudTraslado.gestorConservacionTraslados_id = request.POST['comisario']
        solicitudTraslado.gestorPatrimonio_id = request.POST['comisario']
        solicitudTraslado.fechaSalidaProgramada = request.POST['fechaSalidaProgramada']
        # solicitudTraslado.fechaRetornoProgramada = request.POST['fechaRetornoProgramada']
        solicitudTraslado.numeroResolucion = request.POST['nResolucion']
        solicitudTraslado.save()

        if request.POST['lista']:
            solicitudTraslado.patrimonios.clear()
            patrimoniosSolicitados = list(request.POST['lista'].split(","))
            for idPatrimonio in patrimoniosSolicitados:
                solicitudTraslado.patrimonios.add(Patrimonio.objects.get(pk=idPatrimonio))

            #
        # for f in request.FILES.getlist('file'):
        #     doc = Documento.objects.create(url=f)
        #     DocumentoPorSolicitud.objects.create(documento_id=doc.pk, solicitud_id=solicitudTraslado.pk)
        return redirect('list_transfers')
    else:
        media_path = MEDIA_URL
        traslado = SolicitudTraslado.objects.get(pk=pk)
        entidades = EntidadSolicitante.objects.filter()
        comisarios = User.objects.filter(groups__name="Gestor de Conservacion y Traslados")

        # Nota, se debe considerar los patrominos del traslado
        patrimonios = traslado.patrimonios.all()
        lista = list(patrimonios.values_list('pk', flat=True))
        print(lista)
        documentos = DocumentoPorSolicitud.objects.filter(solicitud_id=traslado.pk)

        estadosEditables = []
        if (traslado.estado == '1'):
            estadosEditables = [('2', 'Evaluar')]
        elif (traslado.estado == '2'):
            estadosEditables = [('3', 'Rechazar'), ('4', 'Aprobar')]
        elif (traslado.estado == '4'):
            estadosEditables = [('5', 'Ejecutar')]
        elif (traslado.estado == '5'):
            estadosEditables = [('6', 'Finalizar')]

        operacion = 'editar'
        idEditar = pk
        context = {
            'traslado': traslado,
            'entidades': entidades,
            'comisarios': comisarios,
            'patrimonios': patrimonios,
            'documentos': documentos,
            'media_path': media_path,
            'estadosEditables': estadosEditables,
            'operacion': operacion,
            'idEditar': idEditar,
            'lista': lista
        }

        return render(request, 'traslado/transfer_add.html', context)


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

    solicitante = EntidadSolicitante.objects.create(doiSolicitante=doiSolicitante, nombreSolicitante=nombreSolicitante,
                                                    correo=correo, direccion=direccion, pais=pais, telefono=telefono)

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
    trasladopk = request.POST.get('traslado_pk')
    traslado = SolicitudTraslado.objects.get(pk=trasladopk)

    nuevo_estado = ''
    if (traslado.estado == '1'):
        nuevo_estado = '2'
    elif (traslado.estado == '2'):
        nuevo_estado = request.POST.get('nuevo_estado')  # puede ser 3 o 4
    elif (traslado.estado == '4'):
        nuevo_estado = '5'
    elif (traslado.estado == '5'):
        nuevo_estado = '6'

    detalle_rechazo = request.POST.get('detalle_rechazo')
    traslado.estado = nuevo_estado
    mensaje = ''

    asunto = ''
    if (nuevo_estado == '3'):
        asunto = 'Aprobación de solicitud de traslado ' + traslado.numeroResolucion
        traslado.detalleRechazo = detalle_rechazo
        mensaje = 'Su solicitud de traslado ha sido rechazada de debido al siguiente motivo: ' + detalle_rechazo
    elif (nuevo_estado == '4'):
        asunto = 'Desaprobación de solicitud de traslado ' + traslado.numeroResolucion
        mensaje = 'Su solicitud de traslado ha sido aceptada de manera satisfactoria'

    traslado.save()

    correo = traslado.entidadSolicitante.correo
    asunto: "Estado de solicitud"

    if (nuevo_estado == '3' or nuevo_estado == '4'):
        send_form_email(asunto, correo, mensaje)

    return JsonResponse({}, status=200)


def actualizarEstado2(request):
    trasladopk = request.POST.get('traslado_pk')
    traslado = SolicitudTraslado.objects.get(pk=trasladopk)

    nuevo_estado = ''
    patrimonios = traslado.patrimonios.all()

    if (traslado.estado == '1'):
        nuevo_estado = '2'
    elif (traslado.estado == '4'):
        nuevo_estado = '5'
        print('>>>>>>>>>>>>>>>>>Dentro ed actualizar esatdo de patrimonios a inactivo>>>>>>>>>>>>>>>>>>>>>>>>>')
        for patrimonio in patrimonios:  # se actualiza el estado de todos los patrimonios de la solicitud
            patrimonio.estado = '2'  # estado no disponible
            patrimonio.save()
    elif (traslado.estado == '5'):
        nuevo_estado = '6'
        print('>>>>>>>>>>>>>>>>>Dentro ed actualizar esatdo de patrimonios a inactivo>>>>>>>>>>>>>>>>>>>>>>>>>')
        for patrimonio in patrimonios:  # se actualiza el estado de todos los patrimonios de la solicitud
            patrimonio.estado = '1'  # estado disponible
            patrimonio.save()

    traslado.estado = nuevo_estado
    traslado.save()
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
