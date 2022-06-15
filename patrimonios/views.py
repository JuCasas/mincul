from django.core import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from patrimonios.models import Patrimonio
from django.http import HttpResponseRedirect
from django.urls import reverse
from patrimonios.models import PatrimonioValoracion, Patrimonio
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from authentication.models import User
from patrimonios.models import Patrimonio, Institucion
from patrimonios.serializers import InstitucionSerializer, UserSerializer

def patrimonio_list(request):

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
    context = {
        'patrimonio': patrimonio,
    }
    return render(request, 'patrimonio/patrimony_edit.html', context)

def detalle(request, pk):
    valor = Patrimonio.objects.get(pk=pk)
    valoraciones = PatrimonioValoracion.objects.filter(patrimonio_id=pk).filter(estado=2)
    puntuacion=0
    for v in valoraciones:
        puntuacion = v.valoracion + puntuacion

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

@method_decorator(csrf_exempt)
def send_email(request, pk):
    url = "http://localhost:8000/patrimonios/email/"+str(pk)
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
    if int(pk) == 1:
        return render(request, 'patrimonio/patrimony_inmueble_edit.html', context)
    else:
        return render(request, 'patrimonio/patrimony_inmaterial_edit.html', context)
