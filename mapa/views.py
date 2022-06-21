from django.shortcuts import render
from patrimonios.models import Patrimonio
from patrimonios.models import  Categoria
from django.http import JsonResponse
# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    context={
        'patrimony':patrimonio
    }
    return render(request,'map/ficha.html',context)

def mapaPatrimonioSimple(request):
    success=-1
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonioNombre.rstrip()
        patrimonioNombre.lstrip()
        success=0
        if patrimonioNombre != '' or patrimonioNombre != None or patrimonioNombre != ' '\
                or patrimonioNombre != "" or patrimonioNombre != " ":
            patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre)
            if len(patrimonios) > 0:
                patrimonio0 = patrimonios[0]
                success=1
                context = {
                    'patrimonios': patrimonios,
                    'patrimonio0': patrimonio0,
                    'lensearch':len(patrimonios),
                    'success':success
                }
                return render(request, 'map/mapaBusquedaSimplePatrimonio.html', context)
            return render(request, 'map/mapaBusquedaSimplePatrimonio.html', {'success':success})
    return render(request, 'map/mapaBusquedaSimplePatrimonio.html',{'success':success})

def mapaPatrimonioAvanzado(request):
    categorias = Categoria.objects.all()
    dep = Patrimonio.objects.all().distinct('departamento')
    departamentos = []
    for d in dep:
        departamentos.append(d.departamento)
    success=-1
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonioCategoria = request.POST['select_categoria']
        patrimoniodepartamento = request.POST['select_departamento']
        patrimonioprovincia = request.POST['select_provincia']
        patrimoniodistrito = request.POST['select_distrito']
        patrimonioNombre.rstrip()
        patrimonioNombre.lstrip()
        success=0
        if patrimonioNombre != '' or patrimonioNombre != None or patrimonioNombre != ' '\
            or patrimonioNombre != "" or patrimonioNombre != " ":
            patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre)
            if len(patrimonios) > 0:
                if(patrimonioCategoria=="Categoría"):
                    pass
                else:
                    cats = Categoria.objects.get(nombre__contains=patrimonioCategoria)
                    catId = cats.pk
                    patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre,
                                                            categoria_id=catId)
                if len(patrimonios)>0:
                    if(patrimoniodepartamento == "Departamento"):
                        pass
                    else:
                        deps = []
                        for p in patrimonios:
                            if (p.departamento==patrimoniodepartamento):
                                deps.append(p)
                        patrimonios=deps
                if len(patrimonios)>0:
                    if(patrimonioprovincia=="Provincia"):
                        pass
                    else:
                        prov = []
                        for p in patrimonios:
                            if (p.provincia==patrimonioprovincia):
                                prov.append(p)
                        patrimonios=prov
                if (len(patrimonios)>0):
                    if(patrimoniodistrito=="Distrito"):
                        pass
                    else:
                        dis = []
                        for p in patrimonios:
                            if (p.distrito==patrimoniodistrito):
                                dis.append(p)
                        patrimonios=dis
                if(len(patrimonios)>0):
                    success = 1
                    patrimonio0 = patrimonios[0]
                    context = {
                        'categorias': categorias,
                        'departamentos': departamentos,
                        'patrimonios': patrimonios,
                        'patrimonio0': patrimonio0,
                        'lensearch': len(patrimonios),
                        'success': success
                    }
                    return render(request, 'map/mapaBusquedaAvzPatrimonio.html', context)
    context = {
        'categorias': categorias,
        'departamentos': departamentos,
        'success':success
    }
    return render(request, 'map/mapaBusquedaAvzPatrimonio.html',context)

def mapaPunto(request,pk):
    patrimonio=Patrimonio.objects.get(id=pk)
    context = {
        'patrimony':{
            'nombreTituloDenominacion':patrimonio.nombreTituloDemoninacion,
            'lat':patrimonio.lat,
            'long':patrimonio.long
        }
    }
    print(context)
    return JsonResponse(context, status=200)
