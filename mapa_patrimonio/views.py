from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

from random import seed
from random import randint
from random import sample

# Create your views here.
from patrimonios.models import Patrimonio
from patrimonios.models import Institucion


def datos(request):
    success=-1
    print(request)
    print(request.POST)
    patri=Patrimonio.objects.filter(estado=1).filter(tipoPatrimonio=2)
    print(patri)
    if request.POST["latIniMenor"]=="true":
        patri=patri.filter(lat__gte=request.POST["latitudIni"]).filter(lat__lte=request.POST["latitudFin"])
        print("ntro")
        print(patri)
    else:
        patri = patri.filter(lat__gte=request.POST["latitudFin"]).filter(lat__lte=request.POST["latitudIni"])
        print("entro")
        print(patri)
    if request.POST["longIniMenor"]=="true":
        patri = patri.filter(long__gte=request.POST["longitudIni"]).filter(long__lte=request.POST["longitudFin"])
        print("entro2")
        print(patri)
    else:
        patri = patri.filter(long__gte=request.POST["longitudFin"]).filter(long__lte=request.POST["longitudIni"])
        print("entro3")
        print(patri)
    print(patri)
    instit=Institucion.objects.filter(estado=1)
    if request.POST["latIniMenor"]:
        instit =instit.filter(lat__gte=request.POST["latitudIni"]).filter(lat__lte=request.POST["latitudFin"])
    else:
        instit = instit.filter(lat__gte=request.POST["latitudFin"]).filter(lat__lte=request.POST["latitudIni"])
    if request.POST["longIniMenor"]:
        instit = instit.filter(long__gte=request.POST["longitudIni"]).filter(long__lte=request.POST["longitudFin"])
    else:
        instit = instit.filter(long__gte=request.POST["longitudFin"]).filter(long__lte=request.POST["longitudIni"])
    print(instit)
    numPatri = patri.count()
    numInstit = instit.count()
    numPatriInstit = 0
    patriInstit = []
    if (numPatri+numInstit) <= 10:
        numPatriInstit = numPatri + numInstit
        for i in range(numPatri):
            patriInstit.append({
                "id": patri[i].id,
                "lat": patri[i].lat,
                "long": patri[i].long,
                "nombre": patri[i].nombreTituloDemoninacion,
                "url": patri[i].url,
                "tipo": 2,
            })
        for j in range(numInstit):
            patriInstit.append({
                "id": instit[i].id,
                "lat": instit[i].lat,
                "long": instit[i].long,
                "nombre": instit[i].nombre,
                "url": instit[i].url,
                "tipo": 4,
            })
        success = 1
    else:#escoger al azar
        numPatriInstit = 10
        numAzarPatri = randint(0, 9)
        numAzarInstit = 10 - numAzarPatri
        if numPatri < numAzarPatri:
            numAzarPatri = numPatri
            numAzarInstit = 10 - numAzarPatri
        elif numInstit < numAzarInstit:
            numAzarInstit = numInstit
            numAzarPatri = 10 - numAzarInstit
        patrimoniosAzar = sample(list(patri.values()), numAzarPatri)
        institucionesAzar = sample(list(instit.values()), numAzarInstit)
        print(patrimoniosAzar)
        for patriAzar in patrimoniosAzar:
            patriInstit.append({
                "id": patriAzar['id'],
                "lat": patriAzar['lat'],
                "long": patriAzar['long'],
                "nombre": patriAzar['nombreTituloDemoninacion'],
                "url": patriAzar['url'],
                "tipo": 2,
            })
        for institAzar in institucionesAzar:
            patriInstit.append({
                "id": institAzar['id'],
                "lat": institAzar['lat'],
                "long": institAzar['long'],
                "nombre": institAzar['nombre'],
                "url": institAzar['url'],
                "tipo": 4,
            })
        success = 1
    return JsonResponse({'data': patriInstit,
                         'numPatrimonios':numPatriInstit,
                        'success':success},
                        status=200, safe=False)

def patrimonioFueraRuta(request):
    return JsonResponse({'data':'hola'},status=200,safe=False)

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