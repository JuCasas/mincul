from django.shortcuts import render

from patrimonios.models import Servicio
from patrimonios.models import Entrada
from patrimonios.models import ActividadTuristica
from patrimonios.models import Patrimonio
from patrimonios.models import PatrimonioMaterial
from patrimonios.models import PatrimonioMaterialMueble

# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    context={
        'patrimony':patrimonio
    }
    return render(request,'map/ficha.html',context)