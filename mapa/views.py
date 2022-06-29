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
from mincul_app.models import Documento
from django.http import JsonResponse
# Create your views here.

def ficha(request,my_id):
    patrimonio=Patrimonio.objects.get(id=my_id)
    urlPatrimonio = Documento.objects.filter(patrimonio=patrimonio).order_by('id')
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
        try:
            context = {
                'patrimony': patrimonio,
                'patrimonioMuebleData': patrimonioMueble,
                'materialesSecundarios':materialesSecundariosString,
                'tecnicasAcabado': tecnicasAcabadoString,
                'tecnicasDecoracion': tecnicasDecoracionString,
                'tecnicasManufactura': tecnicasManufacturaString,
                'dataCategoria':dataCategoria,
                'urlPatrimonio': '/'+urlPatrimonio[0].url
            }
        except:
            context = {
                'patrimony': patrimonio,
                'patrimonioMuebleData': patrimonioMueble,
                'materialesSecundarios': materialesSecundariosString,
                'tecnicasAcabado': tecnicasAcabadoString,
                'tecnicasDecoracion': tecnicasDecoracionString,
                'tecnicasManufactura': tecnicasManufacturaString,
                'dataCategoria': dataCategoria,
                'urlPatrimonio': '/static/img/landmarks/notAvailable.jpg'
            }
        return render(request, 'map/ficha.html', context)
    context={
        'patrimony':patrimonio,
        'urlPatrimonio':urlPatrimonio[0].url
    }
    return render(request,'map/ficha.html',context)

def mapaPatrimonioSimple(request):
    success=-1
    if request.POST:
        patrimonioNombre = request.POST['patrimonio_name']
        patrimonioNombre.strip()
        if len(patrimonioNombre)>0 :
            success = 0
            patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre,estado="1").exclude(tipoPatrimonio="1")
            if len(patrimonios) > 0:
                instituciones = []
                patri = []
                for p in patrimonios:
                    if int(p.tipoPatrimonio) == 3:
                        insti = Institucion.objects.get(pk=p.institucion.pk)
                        if insti not in instituciones:
                            instiUrl = Documento.objects.filter(institucion=insti).order_by('id')
                            try:
                                instituciones.append({'institucion': insti,
                                                      'url': '/'+instiUrl[0].url})
                            except:
                                instituciones.append({'institucion': insti,
                                                      'url': '/static/img/landmarks/notAvailable.jpg'})

                    else:
                        urlPatrimonio = Documento.objects.filter(patrimonio=p).order_by('id')
                        try:
                            patri.append({'patrimonio':p,
                                          'url':'/'+urlPatrimonio[0].url})
                        except:
                            patri.append({'patrimonio': p,
                                          'url': '/static/img/landmarks/notAvailable.jpg'})
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
    categorias = Categoria.objects.filter().exclude(tipo="1")
    dep = Patrimonio.objects.filter(estado="1").distinct('departamento').exclude(tipoPatrimonio="1")
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
        patrimonioNombre.strip()
        success=0
        patrimonios = Patrimonio.objects.filter(nombreTituloDemoninacion__icontains=patrimonioNombre,estado="1").exclude(tipoPatrimonio="1")
        if len(patrimonios) > 0:
            if(patrimonioCategoria=="Categoría"):
                pass
            else:
                cats = Categoria.objects.get(nombre__iexact=patrimonioCategoria)
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
                            instiUrl = Documento.objects.filter(institucion=insti).order_by('id')
                            try:
                                instituciones.append({'institucion': insti,
                                                      'url': '/'+instiUrl[0].url})
                            except:
                                instituciones.append({'institucion': insti,
                                                      'url': '/static/img/landmarks/notAvailable.jpg'})
                    else:
                        urlPatrimonio = Documento.objects.filter(patrimonio=p).order_by('id')
                        try:
                            patrimons.append({'patrimonio': p,
                                            'url': '/'+urlPatrimonio[0].url})
                        except:
                            patrimons.append({'patrimonio': p,
                                             'url': '/static/img/landmarks/notAvailable.jpg'})
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
        prov = Patrimonio.objects.filter(departamento__exact=dep,estado="1").distinct('provincia')
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
        dis = Patrimonio.objects.filter(provincia__exact=prov,estado="1").distinct('distrito')
        for d in dis:
            distritos.append({'id_representativo': d.pk,
                              'nombreDistrito': d.distrito})
    context = {
        'distritos':distritos
    }
    print(context)
    return JsonResponse(context, status=200)

def patrimonioJson(request,id_patrimonio):
    id_patri = int(id_patrimonio)
    patrimonio = Patrimonio.objects.get(id=id_patri)
    urlPatri = Documento.objects.filter(patrimonio=patrimonio).order_by('id')
    urlPatrimonio=None
    try:
        urlPatrimonio = (urlPatri[0].url)
        urlPatrimonio = '/'+urlPatrimonio.name
    except:
        urlPatrimonio = '/static/img/landmarks/notAvailable.jpg'
    nombre = patrimonio.nombreTituloDemoninacion
    lat = patrimonio.lat
    long = patrimonio.long
    context={
        'nombre':nombre,
        'lat': lat,
        'long': long,
        'url':urlPatrimonio
    }
    return JsonResponse(context,status=200)

def institucionJson(request,id_institucion):
    id_insti = int(id_institucion)
    institucion = Institucion.objects.get(id=id_insti)
    urlInsti = Documento.objects.filter(institucion=institucion).order_by('id')
    urlInstitucion = None
    try:
        urlInstitucion = urlInsti[0].url
        urlInstitucion = '/'+urlInstitucion.name
    except:
        urlInstitucion = '/static/img/landmarks/notAvailable.jpg'
    nombre = institucion.nombre
    lat = institucion.lat
    long = institucion.long
    context={
        'nombre':nombre,
        'lat': lat,
        'long': long,
        'url':urlInstitucion
    }
    return JsonResponse(context,status=200)
