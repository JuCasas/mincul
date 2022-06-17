from django.shortcuts import render
from patrimonios.models import Patrimonio
from django.http import JsonResponse
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
        patrimonioNombre.rstrip()
        patrimonioNombre.lstrip()
        if patrimonioNombre != '' or patrimonioNombre != None or patrimonioNombre != ' '\
                or patrimonioNombre != "" or patrimonioNombre != " ":
            patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre)
            if len(patrimonios) > 0:
                patrimonio0 = patrimonios[0]
                context = {
                    'patrimonios': patrimonios,
                    'patrimonio0': patrimonio0
                }
                return render(request, 'map/mapaBusquedaSimplePatrimonio.html', context)
    return render(request, 'map/mapaBusquedaSimplePatrimonio.html')

def mapaPatrimonioAvanzado(request):
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonioCategoria = request.POST['select_categoria']
        patrimoniodepartamento = request.POST['select_departamento']
        patrimonioprovincia = request.POST['select_provincia']
        patrimoniodistrito = request.POST['select_distrito']
        patrimonioNombre.rstrip()
        patrimonioNombre.lstrip()
        if patrimonioNombre != '' or patrimonioNombre != None or patrimonioNombre != ' '\
            or patrimonioNombre != "" or patrimonioNombre != " ":
            patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre)
            patriNom=[]
            patriDep=[]
            patriProv=[]
            patriDis=[]
            if len(patrimonios) > 0:
                for p in patrimonios:
                    if p.categoria.pk == 1 and patrimonioCategoria == "Mueble":
                        patriNom.append(p)
                    elif p.categoria.pk == 2 and patrimonioCategoria == "Inmueble":
                        patriNom.append(p)
                    elif patrimonioCategoria == "Categoría":
                        patriNom.append(p)
                if len(patriNom) >0:
                    for p in patriNom:
                        if p.departamento == patrimoniodepartamento:
                            patriDep.append(p)
                        elif patrimoniodepartamento == "Departamento":
                            patriDep.append(p)
                    if len(patriDep)>0:
                        for p in patriDep:
                            if p.provincia == patrimonioprovincia:
                                patriProv.append(p)
                            elif patrimonioprovincia == 'Provincia':
                                patriProv.append(p)
                        if len(patriProv) > 0:
                            for p in patriProv:
                                if p.provincia == patrimonioprovincia:
                                    patriDis.append(p)
                                elif patrimonioprovincia == 'Provincia':
                                    patriDis.append(p)
                            if len(patriDis) > 0:
                                patriFinal=[]
                                if patrimoniodistrito!="Distrito":
                                    for p in patriDis:
                                        if p.distrito == patrimoniodistrito:
                                            patriFinal.append(p)
                                    if len(patriFinal)>0:
                                        patrimonio0 = patriFinal[0]
                                        context = {
                                            'patrimonios': patriFinal,
                                            'patrimonio0': patrimonio0
                                        }
                                        return render(request, 'map/mapaBusquedaAvzPatrimonio.html', context)
                                else:
                                    patrimonio0 = patriDis[0]
                                    context = {
                                        'patrimonios': patriDis,
                                        'patrimonio0': patrimonio0
                                    }
                                    return render(request, 'map/mapaBusquedaAvzPatrimonio.html',context)
    return render(request, 'map/mapaBusquedaAvzPatrimonio.html')

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
