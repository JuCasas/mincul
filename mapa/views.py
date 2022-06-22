from django.shortcuts import render
from patrimonios.models import Patrimonio
from patrimonios.models import  Categoria
from patrimonios.models import Institucion
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
                instituciones = []
                patriInmueble = []
                for p in patrimonios:
                    if int(p.tipoPatrimonio) == 3:
                        insti = Institucion.objects.get(pk=p.institucion.pk)
                        if insti not in instituciones:
                            instituciones.append(insti)
                    if int(p.tipoPatrimonio) == 2:
                        patriInmueble.append(p)
                patrimonio0 = None
                institucion0 = None
                if len(patriInmueble)>0:
                    patrimonio0 = patriInmueble[0]
                if len(instituciones)>0:
                    institucion0 = instituciones[0]
                success=1
                context = {
                    'patrimonios': patriInmueble,
                    'instituciones':instituciones,
                    'patrimonio0': patrimonio0,
                    'institucion0':institucion0,
                    'lensearch':len(patriInmueble)+len(instituciones),
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
        departamentos.append({'id_representativo':d.pk,
                              'nombreDepartamento':d.departamento})
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
                    patriId = int(patrimoniodepartamento)
                    if(patriId == -1):
                        pass
                    else:
                        patri = Patrimonio.objects.get(id=patriId)
                        patriDepa = patri.departamento
                        deps = []
                        for p in patrimonios:
                            if (p.departamento==patriDepa):
                                deps.append(p)
                        patrimonios=deps
                if len(patrimonios)>0:
                    provId = int(patrimonioprovincia)
                    if(provId == -1):
                        pass
                    else:
                        patri = Patrimonio.objects.get(id=provId)
                        patriProv = patri.provincia
                        prov = []
                        for p in patrimonios:
                            if (p.provincia==patriProv):
                                prov.append(p)
                        patrimonios=prov
                if (len(patrimonios)>0):
                    distId=int(patrimoniodistrito)
                    if(distId == -1):
                        pass
                    else:
                        dis = []
                        patri = Patrimonio.objects.get(id=distId)
                        patriDis = patri.distrito
                        for p in patrimonios:
                            if (p.distrito==patriDis):
                                dis.append(p)
                        patrimonios=dis
                if(len(patrimonios)>0):
                    instituciones = []
                    patriInmueble = []
                    for p in patrimonios:
                        if int(p.tipoPatrimonio) == 3:
                            insti = Institucion.objects.get(pk=p.institucion.pk)
                            if insti not in instituciones:
                                instituciones.append(insti)
                        if int(p.tipoPatrimonio) == 2:
                            patriInmueble.append(p)
                    patrimonio0 = None
                    institucion0 = None
                    if len(patriInmueble) > 0:
                        patrimonio0 = patriInmueble[0]
                    if len(instituciones) > 0:
                        institucion0 = instituciones[0]
                    success = 1
                    context = {
                        'categorias': categorias,
                        'departamentos': departamentos,
                        'patrimonios': patriInmueble,
                        'instituciones':instituciones,
                        'patrimonio0': patrimonio0,
                        'institucion0':institucion0,
                        'lensearch': len(patriInmueble)+len(instituciones),
                        'success': success
                    }
                    return render(request, 'map/mapaBusquedaAvzPatrimonio.html', context)
    context = {
        'categorias': categorias,
        'departamentos': departamentos,
        'success':success
    }
    return render(request, 'map/mapaBusquedaAvzPatrimonio.html',context)

def provinciaJson(request,id_representativo):
    provincias = []
    id_representativo = int(id_representativo)
    if id_representativo != -1:
        patrimonioEjemplo = Patrimonio.objects.get(id=id_representativo)
        dep = patrimonioEjemplo.departamento
        prov = Patrimonio.objects.filter(departamento__exact=dep).distinct('provincia')
        for p in prov:
            provincias.append({'id_representativo': p.pk,
                              'nombreProvincia': p.provincia})
    context = {
        'provincias': provincias
    }
    print(context)
    return JsonResponse(context, status=200)

def distritoJson(request,id_representativo):
    distritos = []
    id_representativo = int(id_representativo)
    if id_representativo!=-1:
        patrimonioEjemplo=Patrimonio.objects.get(id=id_representativo)
        prov = patrimonioEjemplo.provincia
        dis = Patrimonio.objects.filter(provincia__exact=prov).distinct('distrito')
        for d in dis:
            distritos.append({'id_representativo': d.pk,
                              'nombreDistrito': d.distrito})
    context = {
        'distritos':distritos
    }
    print(context)
    return JsonResponse(context, status=200)