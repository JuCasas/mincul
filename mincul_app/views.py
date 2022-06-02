from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from patrimonios.models import PatrimonioValoracion

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.
def template(request):
    return render(request, 'template_auth.html')

def detalle(request):
    context = {'puntacion':4}

    if request.POST:
        print(request.POST)
        valoracion = PatrimonioValoracion.objects.create()
        #falta la conexion con detalle del patrimonio, coordinar con el grupo encargado
        valoracion.nombre = request.POST.get("name")
        valoracion.correo = request.POST.get("email")
        valoracion.comentario = request.POST.get("comment")
        valoracion.valoracion = request.POST.get("score")
        valoracion.save()
        send_email(request)
        return HttpResponseRedirect(reverse(detalle))
    return render(request, 'templateDetail.html', context)

def login(request):
    return render(request, 'patrimonio/patrimony_list.html')

def material(request):
    return render(request, 'materialKit.html')

@method_decorator(csrf_exempt)
def send_email(request):
    if request.POST:
        try:
            subject = "Confirma tu correo electrónico"
            sender = 'info@inova.team'

            #enviar enlace a una vista de confirmacion
            context = {
                'url_val': 'hola'
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
