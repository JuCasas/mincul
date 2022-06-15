from django.shortcuts import render
from patrimonios.models import Patrimonio

# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    context={
        'patrimony':patrimonio
    }
    return render(request,'map/ficha.html',context)

def mapaPatrimonio(request):
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonio = Patrimonio.objects.get(nombreTituloDemoninacion=patrimonioNombre)
        return render(request, 'map/mapaBusquedaPatrimonio.html', {'patrimonio':patrimonio})
    else:
        return render(request, 'map/mapaBusquedaPatrimonio.html',{})