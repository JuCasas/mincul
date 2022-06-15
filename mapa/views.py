from django.shortcuts import render
from patrimonios.models import Patrimonio

# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    context={
        'patrimony':patrimonio
    }
    return render(request,'map/ficha.html',context)

def mapaPatrimonioSimple(request):
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonio = None
        print(":::")
        print(patrimonioNombre)
        print(":::")
        if patrimonioNombre != '' or patrimonioNombre != None:
            patrimonio = Patrimonio.objects.get(nombreTituloDemoninacion=patrimonioNombre)
            return render(request, 'map/mapaBusquedaSimplePatrimonio.html', {'patrimonio': patrimonio})
    return render(request, 'map/mapaBusquedaSimplePatrimonio.html', {})

def mapaPatrimonioAvanzado(request):
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonio = None
        print(":::")
        print(patrimonioNombre)
        print(":::")
        if patrimonioNombre != '' or patrimonioNombre != None:
            patrimonio = Patrimonio.objects.get(nombreTituloDemoninacion=patrimonioNombre)
            return render(request, 'map/mapaBusquedaAvzPatrimonio.html', {'patrimonio': patrimonio})
    return render(request, 'map/mapaBusquedaAvzPatrimonio.html', {})