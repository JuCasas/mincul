from django.shortcuts import render
from patrimonios.models import Patrimonio
from patrimonios.models import Categoria
from patrimonios.models import Institucion
from patrimonios.models import PatrimonioMaterialMueble
from patrimonios.models import PatrimonioEtnografico
from patrimonios.models import PatrimonioIndustrial
from patrimonios.models import PatrimonioArqueologico
from patrimonios.models import PatrimonioPaleontologico
from patrimonios.models import PatrimonioHistoricoArtistico
from django.http import JsonResponse
# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    if patrimonio.tipoPatrimonio == "3":
        patrimonioMueble = PatrimonioMaterialMueble.objects.get(patrimonio=patrimonio)
        materialesSecundarios = patrimonioMueble.materialesSecundarios.all()
        tecnicasAcabado = patrimonioMueble.tecnicasAcabado.all()
        tecnicasDecoracion = patrimonioMueble.tecnicasDecoracion.all()
        tecnicasManufactura = patrimonioMueble.tecnicasManifactura.all()
        materialesSecundariosString =''
        tecnicasAcabadoString = ''
        tecnicasDecoracionString = ''
        tecnicasManufacturaString = ''
        i=0
        for e in materialesSecundarios:
            if i == 0:
                materialesSecundariosString = e.descripcion
            else:
                materialesSecundariosString = materialesSecundariosString + ', ' + e.descripcion
            i += 1
        i = 0
        for e in tecnicasAcabado:
            if i == 0:
                tecnicasAcabadoString = e.descripcion
            else:
                tecnicasAcabadoString = tecnicasAcabadoString + ', ' + e.descripcion
            i += 1
        i = 0
        for e in tecnicasDecoracion:
            if i == 0:
                tecnicasDecoracionString = e.descripcion
            else:
                tecnicasDecoracionString = tecnicasDecoracionString + ', ' + e.descripcion
            i += 1
        i = 0
        for e in tecnicasManufactura:
            if i == 0:
                tecnicasManufacturaString = e.descripcion
            else:
                tecnicasManufacturaString = tecnicasManufacturaString + ', ' + e.descripcion
            i += 1
        dataCategoria =  None
        if (patrimonio.categoria.pk == 6):
            dataCategoria = PatrimonioArqueologico.objects.get(patrimonioMueble=patrimonioMueble)
        if (patrimonio.categoria.pk == 7):
            dataCategoria = PatrimonioHistoricoArtistico.objects.get(patrimonioMueble=patrimonioMueble)
        if (patrimonio.categoria.pk == 8):
            dataCategoria = PatrimonioEtnografico.objects.get(patrimonioMueble=patrimonioMueble)
        if (patrimonio.categoria.pk == 9):
            dataCategoria = PatrimonioPaleontologico.objects.get(patrimonioMueble=patrimonioMueble)
        if (patrimonio.categoria.pk == 10):
            dataCategoria = PatrimonioIndustrial.objects.get(patrimonioMueble=patrimonioMueble)
        context = {
            'patrimony': patrimonio,
            'patrimonioMuebleData': patrimonioMueble,
            'materialesSecundarios':materialesSecundariosString,
            'tecnicasAcabado': tecnicasAcabadoString,
            'tecnicasDecoracion': tecnicasDecoracionString,
            'tecnicasManufactura': tecnicasManufacturaString,
            'dataCategoria':dataCategoria
        }
        return render(request, 'map/ficha.html', context)
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
                patri = []
                for p in patrimonios:
                    if int(p.tipoPatrimonio) == 3:
                        insti = Institucion.objects.get(pk=p.institucion.pk)
                        if insti not in instituciones:
                            instituciones.append(insti)
                    else:
                        patri.append(p)
                patrimonio0 = None
                institucion0 = None
                if len(patri)>0:
                    patrimonio0 = patri[0]
                if len(instituciones)>0:
                    institucion0 = instituciones[0]
                success=1
                context = {
                    'patrimonios': patri,
                    'instituciones':instituciones,
                    'patrimonio0': patrimonio0,
                    'institucion0':institucion0,
                    'lensearch':len(patri)+len(instituciones),
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
                    patrimons = []
                    for p in patrimonios:
                        if int(p.tipoPatrimonio) == 3:
                            insti = Institucion.objects.get(pk=p.institucion.pk)
                            if insti not in instituciones:
                                instituciones.append(insti)
                        else:
                            patrimons.append(p)
                    patrimonio0 = None
                    institucion0 = None
                    if len(patrimons) > 0:
                        patrimonio0 = patrimons[0]
                    if len(instituciones) > 0:
                        institucion0 = instituciones[0]
                    success = 1
                    context = {
                        'categorias': categorias,
                        'departamentos': departamentos,
                        'patrimonios': patrimons,
                        'instituciones':instituciones,
                        'patrimonio0': patrimonio0,
                        'institucion0':institucion0,
                        'lensearch': len(patrimons)+len(instituciones),
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