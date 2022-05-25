import json
import random
import string

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from conservacion.models import ProyectoConservacion
from django.core.serializers.json import DjangoJSONEncoder
#
# def get_random_string(length):
#     # With combination of lower and upper case
#     return ''.join(random.choice(string.ascii_letters) for i in range(length))
#
# def generate_autor(count):
#     for j in range(count):
#         codigo =  get_random_string(8)
#         nombre = get_random_string(14)
#         descripcion = get_random_string(20)
#         ProyectoConservacion.objects.create(
#             codigo = codigo,
#             nombre = nombre,
#             descripcion = descripcion,
#         )


def Show(request):
    if request.is_ajax():
        print("Datatable")
        inicio = int(request.GET.get('inicio'))
        fin = int(request.GET.get('limite'))
        data = ProyectoConservacion.objects.\
            filter(estado='1',
                   nombre__icontains=request.GET.get('filtro'))\
            .values('codigo','nombre','descripcion')
        list_data = []
        for indice,valor in enumerate(data[inicio:inicio+fin],inicio):
            list_data.append(valor)
        print(list_data)
        data = {
            'length': data.count(),
            'objects':list_data
        }
        return HttpResponse(json.dumps(data),'application/json')
    else:
        print("Render")
        # generate_autor(200)
        return render(request,'proyectoConservacion/list.html')