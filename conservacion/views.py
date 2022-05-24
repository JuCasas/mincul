from django.shortcuts import render

# Create your views here.
from conservacion.models import ProyectoConservacion


def Show(request):
    context = {
        'projects': ProyectoConservacion.objects.filter().all
    }
    return render(request,'proyectoConservacion/list.html',context)