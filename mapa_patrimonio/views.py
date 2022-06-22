from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse


# Create your views here.
from patrimonios.models import Patrimonio


def datos(request):
    print(request)
    print(request.POST)
    print(request.POST["latitudIni"])
    context = list(Patrimonio.objects.values())
    return JsonResponse({'data':context,'instituciones':None}, status=200, safe=False)

def index(request):
    ########################################################################################################################
    # Get HTML Representation of Map Object
    context = {
        "titulo":"titulo",
    }
    return render(request, 'mapa_patrimonio/index.html', context)

def prueba(request):
    context = {
        "probando":"probando",
        "numero":10,
    }
    return JsonResponse(context, status=200)