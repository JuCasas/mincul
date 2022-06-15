from django.shortcuts import render
from patrimonios.models import Patrimonio


# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    context={
        'patrimony':patrimonio
    }
    return render(request,'map/ficha.html',context)

def mapa(request):

    return render(request,'map/mapaBase.html')