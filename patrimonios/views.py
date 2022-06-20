import json
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import User
from mincul.settings import ALLOWED_HOSTS
# Create your views here.
from patrimonios.models import Patrimonio, Institucion, PatrimonioValoracion, Categoria, PatrimonioInMaterial, Entrada, \
    ActividadTuristica, Responsable
from patrimonios.serializers import InstitucionSerializer, UserSerializer


def patrimonio_list(request):

    if request.POST:
        print('POST')
        file = request.FILES['file']
        data = json.load(file)
        beautify = json.dumps(data, indent=4)
        print(beautify)
        for pat in data:
            patrimonio = Patrimonio()
            patrimonio.nombreTituloDemoninacion = pat['nombre']
            patrimonio.codigo = pat['codigo']
            patrimonio.departamento = pat['departamento']
            patrimonio.provincia = pat['provincia']
            patrimonio.distrito = pat['distrito']
            patrimonio.lat = pat['latitud']
            patrimonio.long = pat['longitud']
            patrimonio.descripcion = pat['descripcion']
            patrimonio.observacion = pat['observaciones']
            patrimonio.tipoPatrimonio = Patrimonio.tipoPatrimonio.field.choices[int(cat.tipo) - 1]

            cat = Categoria.objects.get(nombre__icontains=pat['categoria'])
            patrimonio.categoria = cat

            resp = Responsable.objects.filter(nombre=pat['responsable']['nombreResponsable'])
            if len(resp) > 0:
                resp = Responsable.objects.get(nombre=pat['responsable']['nombreResponsable'])
            else:
                resp = Responsable()
                resp.institucion = pat['responsable']['institucionLlenadoFicha']
                resp.nombre = pat['responsable']['nombreResponsable']
                resp.cargo = pat['responsable']['cargo']
                resp.correo = pat['responsable']['correo']
                resp.telefono = pat['responsable']['telefono']
                resp.fecha = datetime.strptime(pat['responsable']['fecha'],"%d/%m/%Y")
                resp.save()
            patrimonio.responsables.add(resp)

            

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'patrimonio/patrimony_list.html', context=context)

@api_view(('GET',))
def instituciones_list_api(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page - 1) * length
    end = start + length
    queryset = Institucion.objects.filter(nombre__icontains=search,estado='1').order_by('nombre')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = InstitucionSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

@api_view(('GET',))
def gestorPatrimonio_list_api(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page - 1) * length
    end = start + length
    queryset = User.objects.filter(first_name__icontains=search).order_by('first_name')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = UserSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

def patrimonio_edit(request,pk):
    patrimonio = -1
    #patrimonio = Patrimonio.objects.get(pk=pk)
    entradas = Entrada.objects.filter()
    actividadesTuristicas = ActividadTuristica.objects.filter()
    if int(pk) == 1:
        categorias = Categoria.objects.filter(tipo=2)
        context = {
            'patrimonio': patrimonio,
            'categorias': categorias,

        }
        return render(request, 'patrimonio/patrimony_inmueble_edit.html', context)
    else:
        categorias = Categoria.objects.filter(tipo=1)
        tiposIngreso = PatrimonioInMaterial.tipoIngreso.field.choices
        context = {
            'patrimonio': patrimonio,
            'categorias': categorias,
            'tiposIngreso': tiposIngreso,
            'entradas': entradas,
            'actividades_turisticas': actividadesTuristicas,
        }
        return render(request, 'patrimonio/patrimony_inmaterial_edit.html', context)

def detalle(request, pk):
    valor = Patrimonio.objects.get(pk=pk)
    valoraciones = PatrimonioValoracion.objects.filter(patrimonio_id=pk).filter(estado=2)
    puntuacion=0
    for v in valoraciones:
        puntuacion = v.valoracion + puntuacion
    if len(valoraciones):
        puntuacion=puntuacion/len(valoraciones)
    context = {'puntacion': puntuacion, 'valor': valor, 'valoraciones': valoraciones}

    if request.POST:
        print(request.POST)
        valoracion = PatrimonioValoracion.objects.create()
        valoracion.patrimonio_id = pk;
        valoracion.nombre = request.POST.get("name")
        valoracion.correo = request.POST.get("email")
        valoracion.comentario = request.POST.get("comment")
        valoracion.valoracion = request.POST.get("score")
        valoracion.save()
        send_email(request, valoracion.pk)
        return HttpResponseRedirect(reverse(detalle, args=[pk]))
    return render(request, 'patrimonio/templateDetail.html', context)

def detalle_museo(request, pk):
    #Provisional hasta cambio de la bd
    #museo
    valor = {'url': 'https://enlima.pe/sites/default/files/mali-lima.jpg',
             'nombre': 'Museo Nacional de Arqueología, Antropología e Historia del Perú'}

    area = {'direccion': 'Plaza Bolivar s/n',
            'departamento': 'Lima',
            'provincia': 'Lima',
            'distrito': 'Pueblo Libre'}

    institucion = Institucion.objects.get(pk=pk)
    #lista de patrimonio dentro del museo
    patrimonios = Patrimonio.objects.filter(institucion_id=pk)

    #lista de valoraciones de esos patrimonios


    #lista de incidentes






    context = {"valor": valor,
               "area": area,
               "institucion": institucion,
               "patrimonios": patrimonios}

    return render(request, 'patrimonio/patrimony_museum.html',context)

@method_decorator(csrf_exempt)
def send_email(request, pk):

    if str(ALLOWED_HOSTS) == "[]":
        url = "http://localhost:8000/patrimonios/email_confirmation/" + str(pk)
    else:
        url = "http://119.8.150.164:8080/patrimonios/email_confirmation/" + str(pk)

    if request.POST:
        try:
            subject = "Confirma tu correo electrónico"
            sender = 'info@inova.team'

            #enviar enlace a una vista de confirmacion
            context = {
                'url_val': url
            }
            template = get_template('patrimonio/patrimony_email.html')
            content = template.render(context)

            correos = [request.POST.get("email")]
            for correo in correos:
                correo = correo.strip()
                email = EmailMultiAlternatives(subject, '', sender, [correo], cc=[])
                email.attach_alternative(content, 'text/html')
                email.send()
            print('Se envió el correo con éxito')
        except Exception as e:
            print(str(e))

def email_confirmation(request, pk):
    valor = PatrimonioValoracion.objects.get(pk=pk)
    print('Hola')
    valor.estado = 2
    print(valor.estado)
    valor.save()
    context = {'valor':valor}
    return render(request, 'patrimonio/email_confirmation.html', context)
