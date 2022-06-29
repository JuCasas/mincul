from django.shortcuts import render, redirect

# Create your views here.
from patrimonios.models import Patrimonio


def template(request):
    return render(request, 'template_auth.html')

def login(request):
    patrimonios = Patrimonio.objects.filter(estado=1).order_by('nombreTituloDemoninacion')

    context = {
        'patrimonios': patrimonios,
        'cantidad': len(patrimonios),
    }

    return render(request, 'patrimonio/patrimony_list.html', context=context)

def material(request):
    return render(request, 'materialKit.html')

def origin(request):
    return redirect('mapaPatrimonioSimple')