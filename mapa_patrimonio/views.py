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
from mincul_app.models import Documento
from patrimonios.models import Patrimonio
from patrimonios.models import Institucion


def datos(request):
    success=-1
    patri=Patrimonio.objects.filter(estado=1).filter(tipoPatrimonio=2)
    if request.POST["latIniMenor"]=="true":
        patri=patri.filter(lat__gte=request.POST["latitudIni"]).filter(lat__lte=request.POST["latitudFin"])
    else:
        patri = patri.filter(lat__gte=request.POST["latitudFin"]).filter(lat__lte=request.POST["latitudIni"])
    if request.POST["longIniMenor"]=="true":
        patri = patri.filter(long__gte=request.POST["longitudIni"]).filter(long__lte=request.POST["longitudFin"])
    else:
        patri = patri.filter(long__gte=request.POST["longitudFin"]).filter(long__lte=request.POST["longitudIni"])
    instit=Institucion.objects.filter(estado=1)
    if request.POST["latIniMenor"]:
        instit =instit.filter(lat__gte=request.POST["latitudIni"]).filter(lat__lte=request.POST["latitudFin"])
    else:
        instit = instit.filter(lat__gte=request.POST["latitudFin"]).filter(lat__lte=request.POST["latitudIni"])
    if request.POST["longIniMenor"]:
        instit = instit.filter(long__gte=request.POST["longitudIni"]).filter(long__lte=request.POST["longitudFin"])
    else:
        instit = instit.filter(long__gte=request.POST["longitudFin"]).filter(long__lte=request.POST["longitudIni"])
    numPatri = patri.count()
    numInstit = instit.count()
    numPatriInstit = 0
    patriInstit = []
    if (numPatri+numInstit) <= 10:
        numPatriInstit = numPatri + numInstit
        for i in range(numPatri):
            try:
                patrUrl = Documento.objects.filter(patrimonio=patri[i]).order_by('id')
                patriUrl = patrUrl[0].url
                patriUrl = patriUrl.name
                patriInstit.append({
                    "id": patri[i].id,
                    "lat": patri[i].lat,
                    "long": patri[i].long,
                    "nombre": patri[i].nombreTituloDemoninacion,
                    "url": patriUrl,
                    "tipo": 2,
                })
            except:
                patriInstit.append({
                    "id": patri[i].id,
                    "lat": patri[i].lat,
                    "long": patri[i].long,
                    "nombre": patri[i].nombreTituloDemoninacion,
                    "url": '/static/img/imageNotAvailable.jpg',
                    "tipo": 2,
                })
        for j in range(numInstit):
            try:
                #instiUrl = Documento.objects.filter(institucion=instit[j]).order_by('id')
                #instiUrl = instiUrl[0].url
                #instiUrl = instiUrl.name
                patriInstit.append({
                    "id": instit[j].id,
                    "lat": instit[j].lat,
                    "long": instit[j].long,
                    "nombre": instit[j].nombre,
                    "url": '/static/img/museos-de-peru.png',
                    "tipo": 4,
                })
            except:
                patriInstit.append({
                    "id": instit[i].id,
                    "lat": instit[i].lat,
                    "long": instit[i].long,
                    "nombre": instit[i].nombre,
                    "url": '/static/img/imageNotAvailable.jpg',
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
        for patriAzar in patrimoniosAzar:
            try:
                ppatrUrl = Documento.objects.filter(patrimonio__id=patriAzar['id']).order_by('id')
                ppatriUrl = ppatrUrl[0].url
                print(ppatriUrl)
                print(type(ppatriUrl))
                ppatriUrl = ppatriUrl.name
                patriInstit.append({
                    "id": patriAzar["id"],
                    "lat": patriAzar["lat"],
                    "long": patriAzar["long"],
                    "nombre": patriAzar["nombreTituloDemoninacion"],
                    "url": ppatriUrl,
                    "tipo": 2,
                })
            except:
                patriInstit.append({
                    "id": patriAzar["id"],
                    "lat": patriAzar["lat"],
                    "long": patriAzar["long"],
                    "nombre": patriAzar["nombreTituloDemoninacion"],
                    "url": '/static/img/imageNotAvailable.jpg',
                    "tipo": 2,
                })
        for institAzar in institucionesAzar:
            try:
                #instiUrl = Documento.objects.filter(institucion__id=institAzar['id']).order_by('id')
                #instiUrl = instiUrl[0].url
                #print(instiUrl)
                #print(type(instiUrl))
                #instiUrl = instiUrl.name
                patriInstit.append({
                    "id": institAzar.id,
                    "lat": institAzar.lat,
                    "long": institAzar.long,
                    "nombre": institAzar.nombre,
                    "url": '/static/img/museos-de-peru.png',
                    "tipo": 2,
                })
            except:
                patriInstit.append({
                    "id": institAzar.id,
                    "lat": institAzar.lat,
                    "long": institAzar.long,
                    "nombre": institAzar.nombre,
                    "url": '/' + '/static/img/imageNotAvailable.jpg',
                    "tipo": 2,
                })
        success = 1
    return JsonResponse({'data': patriInstit,
                         'numPatrimonios':numPatriInstit,
                        'success':success},
                        status=200, safe=False)

def patrimonioFueraRuta(request):
    print(request.POST)
    idPatrimonios=request.POST.getlist("idPatrimoniosEnrutados[]")
    idInstituciones = request.POST.getlist("idInstitucionesEnrutadas[]")
    print(idPatrimonios)
    print(idInstituciones)
    patri = Patrimonio.objects.filter(estado=1).filter(tipoPatrimonio=2)
    patri = patri.filter(lat__gte=request.POST["suresteLat"]).filter(lat__lte=request.POST["noroesteLat"])
    patri = patri.filter(long__gte=request.POST["noroesteLong"]).filter(long__lte=request.POST["suresteLong"])
    instit = Institucion.objects.filter(estado=1)
    instit = instit.filter(lat__gte=request.POST["suresteLat"]).filter(lat__lte=request.POST["noroesteLat"])
    instit = instit.filter(long__gte=request.POST["noroesteLong"]).filter(long__lte=request.POST["suresteLong"])

    for idPatri in idPatrimonios:
        patri=patri.exclude(id=int(idPatri))
    for idInstit in idInstituciones:
        instit=instit.exclude(id=int(idInstit))

    numEnrutados=request.POST.get("numEnrutados")
    numEnrutados=int(numEnrutados)
    numPatri = patri.count()
    numInstit = instit.count()
    numPatriInstit = 0
    patriInstit = []
    if (numPatri + numInstit) <= numEnrutados:
        numPatriInstit = numPatri + numInstit
        for i in range(numPatri):
            try:
                patrUrl = Documento.objects.filter(patrimonio=patri[i]).order_by('id')
                patriUrl = patrUrl[0].url
                patriUrl = patriUrl.name
                patriInstit.append({
                    "id": patri[i].id,
                    "lat": patri[i].lat,
                    "long": patri[i].long,
                    "nombre": patri[i].nombreTituloDemoninacion,
                    "url": patriUrl,
                    "tipo": 2,
                })
            except:
                patriInstit.append({
                    "id": patri[i].id,
                    "lat": patri[i].lat,
                    "long": patri[i].long,
                    "nombre": patri[i].nombreTituloDemoninacion,
                    "url": '/static/img/imageNotAvailable.jpg',
                    "tipo": 2,
                })
        for j in range(numInstit):
            try:
                #instiUrl = Documento.objects.filter(institucion=instit[j]).order_by('id')
                #instiUrl = instiUrl[0].url
                #instiUrl = instiUrl.name
                patriInstit.append({
                    "id": instit[j].id,
                    "lat": instit[j].lat,
                    "long": instit[j].long,
                    "nombre": instit[j].nombre,
                    "url": '/static/img/museos-de-peru.png',
                    "tipo": 4,
                })
            except:
                patriInstit.append({
                    "id": instit[j].id,
                    "lat": instit[j].lat,
                    "long": instit[j].long,
                    "nombre": instit[j].nombre,
                    "url": '/static/img/imageNotAvailable.jpg',
                    "tipo": 4,
                })
        success = 1
    else:  # escoger al azar
        numPatriInstit = numEnrutados
        numAzarPatri = randint(0, numEnrutados)
        numAzarInstit = numEnrutados - numAzarPatri
        if numPatri < numAzarPatri:
            numAzarPatri = numPatri
            numAzarInstit = numEnrutados - numAzarPatri
        elif numInstit < numAzarInstit:
            numAzarInstit = numInstit
            numAzarPatri = numEnrutados - numAzarInstit
        patrimoniosAzar = sample(list(patri.values()), numAzarPatri)
        institucionesAzar = sample(list(instit.values()), numAzarInstit)
        for patriAzar in patrimoniosAzar:
            try:
                ppatrUrl = Documento.objects.filter(patrimonio__id=patriAzar['id']).order_by('id')
                ppatriUrl = ppatrUrl[0].url
                print(ppatriUrl)
                print(type(ppatriUrl))
                ppatriUrl = ppatriUrl.name
                patriInstit.append({
                    "id": patriAzar["id"],
                    "lat": patriAzar["lat"],
                    "long": patriAzar["long"],
                    "nombre": patriAzar["nombreTituloDemoninacion"],
                    "url": ppatriUrl,
                    "tipo": 2,
                })
            except:
                patriInstit.append({
                    "id": patriAzar["id"],
                    "lat": patriAzar["lat"],
                    "long": patriAzar["long"],
                    "nombre": patriAzar["nombreTituloDemoninacion"],
                    "url": '/static/img/imageNotAvailable.jpg',
                    "tipo": 2,
                })
        for institAzar in institucionesAzar:
            try:
                #instiUrl = Documento.objects.filter(institucion__id=institAzar['id']).order_by('id')
                #instiUrl = instiUrl[0].url
                #print(instiUrl)
                #print(type(instiUrl))
                #instiUrl = instiUrl.name
                patriInstit.append({
                    "id": institAzar.id,
                    "lat": institAzar.lat,
                    "long": institAzar.long,
                    "nombre": institAzar.nombre,
                    "url": '/static/img/museos-de-peru.png',
                    "tipo": 2,
                })
            except:
                patriInstit.append({
                    "id": institAzar.id,
                    "lat": institAzar.lat,
                    "long": institAzar.long,
                    "nombre": institAzar.nombre,
                    "url": '/' + '/static/img/imageNotAvailable.jpg',
                    "tipo": 2,
                })
        success = 1

    return JsonResponse({'data': patriInstit,
                          'success': success},
                        status=200, safe=False)

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