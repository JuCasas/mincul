from django.shortcuts import render

# Create your views here.
from patrimonios.models import Patrimonio
from django.http import HttpResponseRedirect
from django.urls import reverse
from patrimonios.models import PatrimonioValoracion, Patrimonio
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

def patrimonio_list(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'patrimonio/patrimony_list.html', context=context)

def patrimonio_edit(request,pk):
    patrimonio = -1
    #patrimonio = Patrimonio.objects.get(pk=pk)
    context = {
        'patrimonio': patrimonio,
    }
    return render(request, 'patrimonio/patrimony_edit.html', context)

def detalle(request, pk):
    valor = Patrimonio.objects.get(pk=pk)
    context = {'puntacion':4, 'valor':valor}

    if request.POST:
        print(request.POST)
        valoracion = PatrimonioValoracion.objects.create()
        valoracion.patrimonio_id = pk;
        valoracion.nombre = request.POST.get("name")
        valoracion.correo = request.POST.get("email")
        valoracion.comentario = request.POST.get("comment")
        valoracion.valoracion = request.POST.get("score")
        valoracion.save()
        send_email(request, pk)
        return HttpResponseRedirect(reverse(detalle, args=[pk]))
    return render(request, 'patrimonio/templateDetail.html', context)

@method_decorator(csrf_exempt)
def send_email(request, pk):
    url = "http://localhost:8000/patrimonios/email/"+pk
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
    valor.estado = 2
    valor.save()
    context = {'valor':valor}
    return render(request, 'patrimonio/email_confirmation.html', context)
