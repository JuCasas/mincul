from django.shortcuts import render

# Create your views here.
from incidente.models import Incidente
from patrimonios.models import Patrimonio

def incidente_listar(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'incidencia/patrimonio_incidente_listar.html', context=context)


def incidente_detalles(request):

    context = {
        'incidentes': Incidente.objects.all()
    }


    return render(request, 'incidencia/incidente_listar.html', context=context)