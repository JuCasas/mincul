from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.


def index(request):

########################################################################################################################
    # Get HTML Representation of Map Object
    context={
        'latitud': '-11.1',
        'longitud': '-11,1',
    }
    return render(request, 'mapa_patrimonio/index.html', context)