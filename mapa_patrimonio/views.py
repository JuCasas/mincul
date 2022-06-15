from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse


# Create your views here.

def datos(request):
    context = {
        "puntosRuta":[
            {
                "lat": -8.712216,
                "long": -78.22655,
                "nombre": "Caral 1",
                "imagen": "https://peru21.pe/resizer/sIGBs_SDuG7dzC8Zmhnl5pESA_4=/580x330/smart/filters:format(jpeg):quality(75)/cloudfront-us-east-1.images.arcpublishing.com/elcomercio/BLPSJN5UDJBDPIAB2WPD6YPGQY.jpeg",
            },
            {
                "lat": -8.773941,
                "long": -78.12544,
                "nombre": "Caral 2",
                "imagen": "https://i.pinimg.com/originals/0b/67/a4/0b67a4860ec8b7049d4e17564247f1e9.jpg",
            },
        ],
        "puntoMedio":{
            "lat": 0,
            "long": 0,
        },
        "acercamiento":10,
    }
    auxTotal=0
    for puntosDeRuta in context["puntosRuta"]:
        auxTotal = auxTotal + puntosDeRuta["lat"]
    context["puntoMedio"]["lat"] = auxTotal / len(context["puntosRuta"])
    auxTotal=0
    for puntosDeRuta in context["puntosRuta"]:
        auxTotal = auxTotal + puntosDeRuta["long"]
    context["puntoMedio"]["long"] = auxTotal / len(context["puntosRuta"])
    print(context)
    return JsonResponse(context, status=200)


def index(request):
    ########################################################################################################################
    # Get HTML Representation of Map Object
    context = {
        'latitud': '-11.1',
        'longitud': '-11,1',
    }
    return render(request, 'mapa_patrimonio/index.html', context)
