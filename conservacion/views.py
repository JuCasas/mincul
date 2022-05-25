import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from conservacion.models import ProyectoConservacion


def Show(request):
    if request.is_ajax():
        print("Datatable")
        data = ProyectoConservacion.objects.filter(estado='1').values('codigo','nombre','descripcion')
        list_data = []
        for indice,valor in enumerate(data):
            list_data.append(valor)
        print(list_data)
        data = {
            'length': data.count(),
            'objects':list_data
        }
        return HttpResponse(json.dumps(data),'application/json')
    else:
        print("Render")
        return render(request,'proyectoConservacion/list.html')