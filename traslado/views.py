import datetime
import json
import os

from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import User
from traslado.serializers import TrasladoSerializer, PatrimonioSerializer, EntidadSerializer
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

    order_column = SolicitudTraslado.ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
      order_column = '-' + order_column

    if search_value:
        queryset = queryset.filter(entidadSolicitante__nombreSolicitante__icontains=search_value)
    if status_filter:
        queryset = queryset.filter(estado=status_filter)

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }



def query_entities_by_args(**kwargs):
    print(kwargs)
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search_value', None)[0]
    order_column = kwargs.get('order_column', None)[0]
    order = kwargs.get('order', None)[0]

    queryset = EntidadSolicitante.objects.all()

    total = queryset.count()

    order_column = EntidadSolicitante.ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
      order_column = '-' + order_column

    if search_value:
        queryset = queryset.filter(nombreSolicitante__icontains=search_value)

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
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
                                                             tipoTraslado=request.POST['tipoTraslado'],
                                                             gestorConservacionTraslados_id=request.POST['comisario'],
                                                             gestorPatrimonio_id=request.POST['comisario'],
                                                             fechaSalidaProgramada=request.POST[
                                                                 'fechaSalidaProgramada'],
                                                             # fechaRetornoProgramada=request.POST[
                                                             #     'fechaRetornoProgramada'],
                                                             # numeroResolucion=request.POST['nResolucion']
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
        comisarios = User.objects.filter(groups__name="Gestor de Conservación y Traslados")
        patrimonios = Patrimonio.objects.filter()
        operacion = "agregar"
        estado = 0
        idEditar = 0

        context = {
            'entidades': entidades,
            'comisarios': comisarios,
            'operacion': operacion,
            'idEditar': idEditar,
            'estado': estado
        }
        return render(request, 'traslado/transfer_add.html', context)


def listarPatrimoniosTraslado(request):
    filtro = request.GET['q']
    patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=filtro, estado='1', tipoPatrimonio='3')
    serializer = PatrimonioSerializer((patrimonios), many=True)
    ser_instance = json.dumps(serializer.data)
    return JsonResponse({"patrimoniosAjax": ser_instance}, status=200)


def entidadEmail(request):
    #print('***********************************************************************************************************')
    #print(request.POST['entidad'])
    #print('***********************************************************************************************************')
    entidad = EntidadSolicitante.objects.get(pk=request.POST['entidad']).correo
    return JsonResponse({"email": entidad}, status=200)


def validarFechas(request):
    print("######## VALIDAR FECHAS ##########")
    print(request.POST)
    fechaRetorno = request.POST['fechaRetornoReal']
    fechaSalida = request.POST['fechaSalidaReal']
    if (fechaRetorno > fechaSalida):
        return JsonResponse(True, status=200, safe=False)
    else:
        return JsonResponse(False, status=200, safe=False)
    print ('#######################')

def existeResolucion(request):
    print("##############EXISTE RESOLUCION##################")
    print(request.POST)
    print("##############$$$$$$$$$$$$$$$$$##################")
    pk = request.POST['idEditar']
    nResActual = SolicitudTraslado.objects.get(pk=pk).numeroResolucion
    if (nResActual is None):
        print("FALSE")
        return JsonResponse({"existe": False}, status=200)
    else:
        print("TRUE")
        return JsonResponse({"existe": True}, status=200)

def existeFechaSalidaProgramada(request):
    pk = request.POST['idEditar']
    nFechaSalidaProgramada = SolicitudTraslado.objects.get(pk=pk).fechaSalidaProgramada
    if (nFechaSalidaProgramada is None):
        print("FALSE")
        return JsonResponse({"existe": False}, status=200)
    else:
        print("TRUE")
        return JsonResponse({"existe": True}, status=200)

def registrarNumResolucion(request):
    trasladoPK = request.POST['idEditar']
    nResolucion = request.POST['nResolucion']
    traslado = SolicitudTraslado.objects.get(pk=trasladoPK)
    traslado.numeroResolucion = nResolucion
    traslado.save()
    return JsonResponse({}, status=200)

def registrarFechaSalidaReal(request):
    trasladoPK = request.POST['idEditar']
    fechaSalidaReal = request.POST['fechaSalidaReal']
    traslado = SolicitudTraslado.objects.get(pk=trasladoPK)
    traslado.fechaSalidaReal = fechaSalidaReal
    traslado.save()
    return JsonResponse({}, status=200)

def registrarFechaRetornoReal(request):
    trasladoPK = request.POST['idEditar']
    fechaRetornoReal = request.POST['fechaRetornoReal']
    traslado = SolicitudTraslado.objects.get(pk=trasladoPK)
    traslado.fechaRetorno = fechaRetornoReal
    traslado.save()
    return JsonResponse({}, status=200)

def existeFechaSalidaReal(request):
    pk = request.POST['idEditar']
    nFechaSalidaReal = SolicitudTraslado.objects.get(pk=pk).fechaSalidaReal
    if (nFechaSalidaReal is None):
        print("FALSE")
        return JsonResponse({"existe": False}, status=200)
    else:
        print("TRUE")
        return JsonResponse({"existe": True}, status=200)

def existeFechaRetornoReal(request):
    pk = request.POST['idEditar']
    nFechaRetornoReal = SolicitudTraslado.objects.get(pk=pk).fechaRetorno
    if (nFechaRetornoReal is None):
        print("FALSE")
        return JsonResponse({"existe": False}, status=200)
    else:
        print("TRUE")
        return JsonResponse({"existe": True}, status=200)

def validarResolucion(request):
    print("########3INGRESO A VALIDAR RESOLICION#######")
    print(request.POST)
    if (request.POST['estado'] == '1'):
        return JsonResponse(True, status=200, safe=False)
    pk = request.POST['PK']
    #estado = request.POST['estado']
    print(pk)

    nResActual = SolicitudTraslado.objects.get(pk=pk).numeroResolucion
    print("#####################")
    print("EL NRESACTUAL ES: ")
    print(nResActual)
    print("#####################")
    existe = SolicitudTraslado.objects.filter(numeroResolucion=request.POST['numResolucion']).exclude(
                numeroResolucion=nResActual).exists()

    if existe:
        return JsonResponse(False, status=200, safe=False)
    else:
        return JsonResponse(True, status=200, safe=False)

    #existe = False
    #if (estado == 2):
    #    if (pk == '0'):
    #        existe = SolicitudTraslado.objects.filter(numeroResolucion=request.POST['nResolucion']).exists()
    #    else:
    #        nResActual = SolicitudTraslado.objects.get(pk=pk).numeroResolucion
    #        print(nResActual)
    #        existe = SolicitudTraslado.objects.filter(numeroResolucion=request.POST['nResolucion']).exclude(
    #            numeroResolucion=nResActual).exists()

    #print(existe)
    return JsonResponse(True, status=200, safe=False)

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
    comisarios = User.objects.filter(groups__name="Gestor de Conservación y Traslados")

    # Nota, se debe considerar los patrominos del traslado
    patrimonios = traslado.patrimonios.all()
    documentos = DocumentoPorSolicitud.objects.filter(solicitud_id=traslado.pk)
    comisario = User.objects.get(pk = traslado.gestorConservacionTraslados.pk)

    context = {
        'traslado': traslado,
        'entidades': entidades,
        'comisarios': comisarios,
        'patrimonios': patrimonios,
        'documentos': documentos,
        'media_path': media_path,
        'comisario': comisario,
    }

    return render(request, 'traslado/transfer_view.html', context)


def editTransfer(request, pk):
    print(request.POST)
    print("AAAAAAAAAAAAAAAAAAAA")
    solicitudTraslado = SolicitudTraslado.objects.get(pk=pk)
    print("SOLICITUD DE TRASLADO - ESTADO")
    print(solicitudTraslado.estado)
    if request.POST:
        if solicitudTraslado.estado == '1':
            solicitudTraslado.entidadSolicitante_id = request.POST['nombreInstitucion']
            solicitudTraslado.tipoTraslado = request.POST['tipoTraslado']
            solicitudTraslado.destino = request.POST['destino']
            solicitudTraslado.nombreExposicion = request.POST['nombreExposicion']
            solicitudTraslado.pais = request.POST['pais']
            solicitudTraslado.gestorConservacionTraslados_id = request.POST['comisario']
            solicitudTraslado.gestorPatrimonio_id = request.POST['comisario']
            solicitudTraslado.fechaSalidaProgramada = request.POST['fechaSalidaProgramada']
            # solicitudTraslado.fechaRetornoProgramada = request.POST['fechaRetornoProgramada']
        if solicitudTraslado.estado == '2':
            #print("DENTRO DEL ESTADO 2")
            #print(request.POST)
            solicitudTraslado.numeroResolucion = request.POST['nResolucion']
        if solicitudTraslado.estado == '4':
            solicitudTraslado.fechaSalidaReal = request.POST['fechaSalidaReal']
        if solicitudTraslado.estado == '5':
            solicitudTraslado.fechaRetorno = request.POST['fechaRetornoReal']
        solicitudTraslado.save()

        if request.POST['lista']:
            solicitudTraslado.patrimonios.clear()
            patrimoniosSolicitados = list(request.POST['lista'].split(","))
            for idPatrimonio in patrimoniosSolicitados:
                solicitudTraslado.patrimonios.add(Patrimonio.objects.get(pk=idPatrimonio))

        for f in request.FILES.getlist('file'):
            doc = Documento.objects.create(url=f)
            DocumentoPorSolicitud.objects.create(documento_id=doc.pk, solicitud_id=solicitudTraslado.pk)
        return redirect('list_transfers')
    else:
        media_path = MEDIA_URL
        traslado = SolicitudTraslado.objects.get(pk=pk)
        entidades = EntidadSolicitante.objects.filter()
        comisarios = User.objects.filter(groups__name="Gestor de Conservación y Traslados")

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
        estado = traslado.estado
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
            'lista': lista,
            'estado': estado
        }

        return render(request, 'traslado/transfer_add.html', context)


@api_view(('GET',))
def listEntidades(request):
    if request.is_ajax():
        print("HOTASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        entities = query_entities_by_args(**request.GET)
        serializer = EntidadSerializer((entities['items']), many=True)
        result = dict()
        result['data'] = serializer.data
        result['recordsTotal'] = entities['total']
        result['recordsFiltered'] = entities['count']

        print("####################################")
        print(result)
        print("####################################")
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    else:
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
    patrimonios = traslado.patrimonios.all()
    if (nuevo_estado == '3'):
        asunto = 'Aprobación de solicitud de traslado ' + traslado.numeroResolucion
        traslado.detalleRechazo = detalle_rechazo
        mensaje = 'Su solicitud de traslado ha sido rechazada de debido al siguiente motivo: ' + detalle_rechazo
    elif (nuevo_estado == '4'):
        asunto = 'Desaprobación de solicitud de traslado ' + traslado.numeroResolucion
        mensaje = 'Su solicitud de traslado ha sido aceptada de manera satisfactoria'
        for patrimonio in patrimonios:  # se actualiza el estado de todos los patrimonios de la solicitud
            patrimonio.estado = '2'  # estado no disponible
            patrimonio.save()

    traslado.save()

    correo = traslado.entidadSolicitante.correo
    asunto: "Estado de solicitud"

    print("NUEVO ESTADO >>>>>>", nuevo_estado)

    if (nuevo_estado == '3' or nuevo_estado == '4'):
        send_form_email(asunto, correo, mensaje)

    return JsonResponse({'nuevo_estado': nuevo_estado}, status=200)


def actualizarEstado2(request):
    trasladopk = request.POST.get('traslado_pk')
    traslado = SolicitudTraslado.objects.get(pk=trasladopk)

    nuevo_estado = ''
    patrimonios = traslado.patrimonios.all()

    if (traslado.estado == '1'):
        nuevo_estado = '2'
    elif (traslado.estado == '4'):
        nuevo_estado = '5'

    elif (traslado.estado == '5'):
        nuevo_estado = '6'
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
