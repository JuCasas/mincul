import json
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.db.models.lookups import In
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import User
from mincul.settings import ALLOWED_HOSTS
# Create your views here.
from patrimonios.models import Patrimonio, Institucion, PatrimonioValoracion, Categoria, PatrimonioInMaterial, Entrada, \
    ActividadTuristica, Responsable, PuntoGeografico, PatrimonioMaterialInMueble, Servicio, EpocaVisita, \
    FuenteBibliografica, PatrimonioPaleontologico, PatrimonioMaterialMueble, PatrimonioIndustrial, Fabricante, \
    PatrimonioArqueologico, TecnicaManufactura, TecnicaDecoracion, PatrimonioHistoricoArtistico, MaterialSecundario, \
    TecnicaAcabado, PatrimonioEtnografico, Propietario, Excavacion, ElementoAdicional
from incidente.models import Incidente
from patrimonios.serializers import InstitucionSerializer, UserSerializer


def patrimonio_list(request):

    if request.POST:
        file = request.FILES['file']
        data = json.load(file)
        # beautify = json.dumps(data, indent=4)
        # print(beautify)
        for pat in data:
            cat = Categoria.objects.get(nombre__icontains=pat['categoria'])
            npat = []
            if int(cat.tipo) == 1 or int(cat.tipo) == 2:
                npat = Patrimonio.objects.filter(codigo=pat['codigo'])
            else:
                npat = Patrimonio.objects.filter(codigo=pat['nroRegistro'])

            if len(npat) == 0:
                patrimonio = Patrimonio()
                patrimonio.tipoPatrimonio = int(cat.tipo)
                patrimonio.categoria = cat

                if int(cat.tipo) == 1:
                    patrimonio.nombreTituloDemoninacion = pat['nombre']
                    patrimonio.codigo = pat['codigo']
                    patrimonio.departamento = pat['departamento']
                    patrimonio.provincia = pat['provincia']
                    patrimonio.distrito = pat['distrito']
                    patrimonio.descripcion = pat['descripcion']
                    patrimonio.observacion = pat['observaciones']
                    if pat['latitud'] != '':
                        patrimonio.lat = pat['latitud']
                    if pat['longitud'] != '':
                        patrimonio.long = pat['longitud']
                    patrimonio.save()

                    resp = Responsable.objects.filter(nombre=pat['responsable']['nombreResponsable'])
                    if len(resp) > 0:
                        resp = Responsable.objects.get(nombre=pat['responsable']['nombreResponsable'])
                    else:
                        resp = Responsable()
                        resp.institucion = pat['responsable']['institucionLlenadoFicha']
                        resp.nombre = pat['responsable']['nombreResponsable']
                        resp.cargo = pat['responsable']['cargo']
                        resp.correo = pat['responsable']['correo']
                        resp.telefono = pat['responsable']['telefono']
                        resp.fecha = datetime.strptime(pat['responsable']['fecha'], "%d/%m/%Y")
                        resp.save()
                    patrimonio.save()
                    patrimonio.responsables.add(resp)
                    patrimonio.save()

                    if pat['responsable']['fuentesBiblio'] != '':
                        fuente = FuenteBibliografica()
                        fuente.referencia = pat['responsable']['fuentesBiblio']
                        fuente.patrimonio = patrimonio
                        fuente.save()

                    for actividad in pat['actividades']:
                        act = ActividadTuristica()
                        act.descripcion = actividad['actividad']
                        act.tipo = actividad['tipo']
                        act.observacion = actividad['observacion']
                        act.patrimonio = patrimonio
                        act.save()

                    for servicio in pat['servicios']:
                        serv = Servicio()
                        serv.categoria = servicio['servicio']
                        serv.tipo = servicio['tipoServicio']
                        serv.observacion = servicio['observacion']
                        serv.patrimonio = patrimonio
                        serv.save()

                    inmaterial = PatrimonioInMaterial()
                    for key, name in dict(PatrimonioInMaterial.tipoInmaterial.field.choices).items():
                        if name == pat['tipo']:
                            inmaterial.tipoInmaterial = int(key)
                            break
                    inmaterial.subtipo = pat['subtipo']
                    inmaterial.particularidades = pat['particularidades']
                    inmaterial.patrimonio = patrimonio

                    if pat['tipoIngreso'] != {}:
                        inmaterial.tipoIngreso = pat['tipoIngreso']['tipo']
                        for ent in pat['tipoIngreso']['observaciones']:
                            entrada = Entrada()
                            entrada.descripcion = ent[0]
                            entrada.precio = ent[1]
                            entrada.patrimonio = patrimonio
                            entrada.save()
                    inmaterial.save()

                elif int(cat.tipo) == 2:
                    patrimonio.nombreTituloDemoninacion = pat['nombre']
                    patrimonio.departamento = pat['departamento']
                    patrimonio.provincia = pat['provincia']
                    patrimonio.distrito = pat['distrito']
                    patrimonio.descripcion = pat['descripcion']
                    patrimonio.observacion = pat['observaciones']
                    patrimonio.codigo = pat['codigo']
                    if pat['latitud'] != '':
                        patrimonio.lat = pat['latitud']
                    if pat['longitud'] != '':
                        patrimonio.long = pat['longitud']
                    patrimonio.save()

                    resp = Responsable.objects.filter(nombre=pat['responsable']['nombreResponsable'])
                    if len(resp) > 0:
                        resp = Responsable.objects.get(nombre=pat['responsable']['nombreResponsable'])
                    else:
                        resp = Responsable()
                        resp.institucion = pat['responsable']['institucionLlenadoFicha']
                        resp.nombre = pat['responsable']['nombreResponsable']
                        resp.cargo = pat['responsable']['cargo']
                        resp.correo = pat['responsable']['correo']
                        resp.telefono = pat['responsable']['telefono']
                        resp.fecha = datetime.strptime(pat['responsable']['fecha'], "%d/%m/%Y")
                        resp.save()
                    patrimonio.save()
                    patrimonio.responsables.add(resp)
                    patrimonio.save()

                    if pat['responsable']['fuentesBiblio'] != '':
                        fuente = FuenteBibliografica()
                        fuente.referencia = pat['responsable']['fuentesBiblio']
                        fuente.patrimonio = patrimonio
                        fuente.save()

                    for actividad in pat['actividades']:
                        act = ActividadTuristica()
                        act.descripcion = actividad['actividad']
                        act.tipo = actividad['tipo']
                        act.observacion = actividad['observacion']
                        act.patrimonio = patrimonio
                        act.save()

                    for servicio in pat['servicios']:
                        serv = Servicio()
                        serv.categoria = servicio['servicio']
                        serv.tipo = servicio['tipoServicio']
                        serv.observacion = servicio['observacion']
                        serv.patrimonio = patrimonio
                        serv.save()

                    inmueble = PatrimonioMaterialInMueble()
                    for key,name in dict(PatrimonioMaterialInMueble.tipoInmueble.field.choices).items():
                        if name == pat['tipo']:
                            inmueble.tipoInmueble = int(key)
                            break
                    inmueble.subtipo = pat['subtipo']
                    inmueble.particularidades = pat['particularidades']
                    inmueble.estadoActual = pat['estadoActual']
                    inmueble.patrimonio = patrimonio

                    if pat['tipoIngreso'] != {}:
                        inmueble.tipoIngreso = pat['tipoIngreso']['tipo']
                        for ent in pat['tipoIngreso']['observaciones']:
                            entrada = Entrada()
                            entrada.descripcion = ent[0]
                            entrada.precio = ent[1]
                            entrada.patrimonio = patrimonio
                            entrada.save()

                    inmueble.save()

                    if pat['epocaPropicia'] != {}:
                        epoca = EpocaVisita()
                        epoca.epocaPropicia = pat['epocaPropicia']['epoca']
                        epoca.especificacion = pat['epocaPropicia']['especificacion']
                        epoca.horaVisita = pat['epocaPropicia']['horaVisita']
                        epoca.observaciones = pat['epocaPropicia']['observaciones']
                        epoca.patrimonioMaterialInMueble = inmueble
                        epoca.save()

                elif int(cat.tipo) == 3:

                    patrimonio.codigo = pat['nroRegistro']
                    patrimonio.direccion = pat['datosUbicacion']['ubicacionGeografica']['direccion']
                    patrimonio.departamento = pat['datosUbicacion']['ubicacionGeografica']['departamento']
                    patrimonio.provincia = pat['datosUbicacion']['ubicacionGeografica']['provincia']
                    patrimonio.distrito = pat['datosUbicacion']['ubicacionGeografica']['distrito']

                    # if pat['latitud'] != '':
                    #     patrimonio.lat = pat['latitud']
                    # if pat['longitud'] != '':
                    #     patrimonio.long = pat['longitud']

                    patrimonio.descripcion = pat['datosTecnicos']['descripcion']
                    patrimonio.observacion = pat['datosTecnicos']['observaciones']

                    inst = Institucion.objects.filter(nombre=pat['datosPropiedad']['custodio'])
                    if len(inst) > 0:
                        inst = Institucion.objects.get(nombre=pat['datosPropiedad']['custodio'])
                    else:
                        inst = Institucion()
                        inst.nombre = pat['datosPropiedad']['custodio']
                        inst.save()
                    patrimonio.institucion = inst
                    patrimonio.save()

                    prop = Propietario.objects.filter(nombre=pat['datosPropiedad']['propietario']['nombrePropietario'])
                    if len(prop) > 0:
                        prop = Propietario.objects.get(nombre=pat['datosPropiedad']['propietario']['nombrePropietario'])
                    else:
                        prop = Propietario()
                        if pat['datosPropiedad']['tipoPropietario'] == 'jurídica':
                            prop.nombre = pat['datosPropiedad']['propietario']['nombrePropietario']
                            prop.direccion = pat['datosPropiedad']['propietario']['direccion']
                            prop.departamento = pat['datosPropiedad']['propietario']['departamento']
                            prop.provincia = pat['datosPropiedad']['propietario']['provincia']
                            prop.distrito = pat['datosPropiedad']['propietario']['distrito']
                            prop.doi = pat['datosPropiedad']['propietario']['documentoIdentidad']
                            prop.telefono = pat['datosPropiedad']['propietario']['telefono']
                            prop.tipo = '1'
                        else:
                            prop.nombre = pat['datosPropiedad']['propietario']['nombrePropietario']
                            prop.direccion = pat['datosPropiedad']['propietario']['direccion']
                            prop.departamento = pat['datosPropiedad']['propietario']['departamento']
                            prop.provincia = pat['datosPropiedad']['propietario']['provincia']
                            prop.distrito = pat['datosPropiedad']['propietario']['distrito']
                            prop.doi = pat['datosPropiedad']['propietario']['documentoIdentidad']
                            prop.telefono = pat['datosPropiedad']['propietario']['telefono']
                            prop.tipo = '2'
                        prop.save()
                    patrimonio.propietarios.add(prop)
                    patrimonio.save()

                    for fuente in pat['datosTecnicos']['bibliografia']:
                        if fuente != '':
                            fue = FuenteBibliografica()
                            fue.referencia = fuente
                            fue.patrimonio = patrimonio
                            fue.save()

                    mueble = PatrimonioMaterialMueble()
                    mueble.nroRegistro = pat['nroRegistro']
                    mueble.asociacion = pat['asociación']
                    mueble.integridad = pat['datosTecnicos']['integridad']
                    mueble.conservacion = pat['datosTecnicos']['conservacion']
                    mueble.detalleConservacion = pat['datosTecnicos']['detalleConservacion']
                    mueble.detalleTratamiento = pat['datosTecnicos']['detalleTratamiento']
                    mueble.alto = pat['datosTecnicos']['dimensionesYPeso']['alto']
                    mueble.largo = pat['datosTecnicos']['dimensionesYPeso']['largo']
                    mueble.ancho = pat['datosTecnicos']['dimensionesYPeso']['ancho']
                    mueble.espesor = pat['datosTecnicos']['dimensionesYPeso']['espesor']
                    mueble.formaAdquisicion = pat['datosPropiedad']['formaAdquision']
                    mueble.ubicacionEspecifica = pat['datosUbicacion']['ubicacionEspecifica']
                    mueble.situacion = pat['datosUbicacion']['situacion']
                    mueble.codigoPropietario = pat['codigos']['codigoPropietario']
                    mueble.codigoRegistroAnteriorINC = pat['codigos']['codigoRegistroAnteriorINC']
                    mueble.codigoInventario = pat['codigos']['codigoInventarioINC']
                    mueble.otrosCodigos = pat['codigos']['otros']
                    mueble.patrimonio = patrimonio
                    mueble.save()

                    if cat.pk ==6:

                        patrimonio.nombreTituloDemoninacion = pat['datosIdentificacion']['denominacion']
                        patrimonio.save()

                        if pat['datosOrigen']['excavacion']:
                            exc = Excavacion()
                            exc.areaGeografica = pat['datosOrigen']['areaGeografica']
                            exc.clasificacionOrigen = pat['datosOrigen']['clasificacionOrigen']
                            exc.nombreClasificacion = pat['datosOrigen']['nombreClasificacionOrigen']
                            exc.capa = pat['datosOrigen']['capa']
                            exc.unidad = pat['datosOrigen']['unidad']
                            exc.sector = pat['datosOrigen']['sector']
                            exc.patrimonioMueble = mueble
                            exc.save()

                        for tecnica in pat['datosTecnicos']['tecnicasManufactura']:
                            tec = TecnicaManufactura.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaManufactura.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaManufactura()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasManifactura.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasDecoracion']:
                            tec = TecnicaDecoracion.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaDecoracion.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaDecoracion()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasDecoracion.add(tec)
                        mueble.save()

                        arq = PatrimonioArqueologico()
                        arq.material = pat['datosIdentificacion']['material']
                        arq.tipoMaterial = pat['datosIdentificacion']['tipoMaterial']
                        arq.cultura = pat['datosIdentificacion']['cultura']
                        arq.estilo = pat['datosIdentificacion']['estilo']
                        arq.periodo = pat['datosIdentificacion']['periodo']
                        arq.diametroMax = pat['datosTecnicos']['dimensionesYPeso']['diametroMax']
                        arq.diametroMin = pat['datosTecnicos']['dimensionesYPeso']['diametroMin']
                        arq.diametroBase = pat['datosTecnicos']['dimensionesYPeso']['diametroBase']
                        arq.patrimonioMueble = mueble
                        arq.save()

                    elif cat.pk == 7:

                        patrimonio.nombreTituloDemoninacion = pat['datosIdentificacion']['tituloDenominacion']
                        patrimonio.save()

                        if pat['datosOrigen']['excavacion']:
                            exc = Excavacion()
                            exc.areaGeografica = pat['datosOrigen']['areaGeografica']
                            exc.clasificacionOrigen = pat['datosOrigen']['clasificacionOrigen']
                            exc.nombreClasificacion = pat['datosOrigen']['nombreClasificacionOrigen']
                            exc.capa = pat['datosOrigen']['capa']
                            exc.unidad = pat['datosOrigen']['unidad']
                            exc.sector = pat['datosOrigen']['sector']
                            exc.patrimonioMueble = mueble
                            exc.save()

                        if pat['presentaElementosAdicionales']:
                            for elemento in pat['elementosAdicionales']:
                                ele = ElementoAdicional()
                                ele.descripcion = elemento['elemento']
                                ele.material = elemento['material']
                                ele.integridad = elemento['integridadBien']
                                ele.conservacion = elemento['conservacionBien']
                                ele.alto = elemento['alto']
                                ele.largo = elemento['largo']
                                ele.ancho = elemento['ancho']
                                ele.espesor = elemento['espesor']
                                ele.fondo = elemento['fondo']
                                ele.diametro = elemento['diametro']
                                ele.patrimonioMueble = mueble
                                ele.save()

                        for material in pat['datosTecnicos']['materialesSecundarios']:
                            mat = MaterialSecundario.objects.filter(descripcion=material)
                            if len(mat) > 0:
                                mat = MaterialSecundario.objects.get(descripcion=material)
                            else:
                                mat = MaterialSecundario()
                                mat.descripcion = material
                                mat.save()
                            mueble.materialesSecundarios.add(mat)

                        for tecnica in pat['datosTecnicos']['tecnicasManufactura']:
                            tec = TecnicaManufactura.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaManufactura.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaManufactura()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasManifactura.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasDecoracion']:
                            tec = TecnicaDecoracion.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaDecoracion.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaDecoracion()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasDecoracion.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasAcabado']:
                            tec = TecnicaAcabado.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaAcabado.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaAcabado()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasAcabado.add(tec)
                        mueble.save()

                        hist = PatrimonioHistoricoArtistico()
                        hist.estilo = pat['datosIdentificacion']['estilo']
                        hist.procedencia = pat['datosIdentificacion']['estilo']
                        hist.datacion = pat['datosIdentificacion']['estilo']
                        hist.materialSoporte = pat['datosTecnicos']['materialSoporte']
                        hist.fondo = pat['datosTecnicos']['dimensionesYPeso']['fondo']
                        hist.diametro = pat['datosTecnicos']['dimensionesYPeso']['diametro']
                        hist.patrimonioMueble = mueble
                        hist.save()

                    elif cat.pk == 8:

                        patrimonio.nombreTituloDemoninacion = pat['datosIdentificacion']['tituloDenominacion']
                        patrimonio.save()

                        if pat['presentaElementosAdicionales']:
                            for elemento in pat['elementosAdicionales']:
                                ele = ElementoAdicional()
                                ele.descripcion = elemento['elemento']
                                ele.material = elemento['material']
                                ele.integridad = elemento['integridadBien']
                                ele.conservacion = elemento['conservacionBien']
                                ele.alto = elemento['alto']
                                ele.largo = elemento['largo']
                                ele.ancho = elemento['ancho']
                                ele.espesor = elemento['espesor']
                                ele.fondo = elemento['fondo']
                                ele.diametro = elemento['diametro']
                                ele.patrimonioMueble = mueble
                                ele.save()

                        for material in pat['datosTecnicos']['materialesSecundarios']:
                            mat = MaterialSecundario.objects.filter(descripcion=material)
                            if len(mat) > 0:
                                mat = MaterialSecundario.objects.get(descripcion=material)
                            else:
                                mat = MaterialSecundario()
                                mat.descripcion = material
                                mat.save()
                            mueble.materialesSecundarios.add(mat)

                        for tecnica in pat['datosTecnicos']['tecnicasManufactura']:
                            tec = TecnicaManufactura.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaManufactura.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaManufactura()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasManifactura.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasDecoracion']:
                            tec = TecnicaDecoracion.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaDecoracion.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaDecoracion()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasDecoracion.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasAcabado']:
                            tec = TecnicaAcabado.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaAcabado.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaAcabado()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasAcabado.add(tec)
                        mueble.save()

                        etno = PatrimonioEtnografico()
                        etno.filacionCultural = pat['datosIdentificacion']['filacionCultural']
                        etno.procedencia = pat['datosIdentificacion']['procedencia']
                        etno.datacion = pat['datosIdentificacion']['datacion']
                        etno.materialSoporte = pat['datosTecnicos']['materialSoporte']
                        etno.fondo = pat['datosTecnicos']['dimensionesYPeso']['fondo']
                        etno.diametro = pat['datosTecnicos']['dimensionesYPeso']['diametro']
                        etno.patrimonioMueble = mueble
                        etno.save()

                    elif cat.pk == 9:

                        patrimonio.nombreTituloDemoninacion = pat['datosIdentificacion']['denominacion']
                        patrimonio.save()

                        if pat['datosOrigen']['excavacion']:
                            exc = Excavacion()
                            exc.areaGeografica = pat['datosOrigen']['areaGeografica']
                            exc.clasificacionOrigen = pat['datosOrigen']['clasificacionOrigen']
                            exc.nombreClasificacion = pat['datosOrigen']['nombreClasificacionOrigen']
                            exc.capa = pat['datosOrigen']['capa']
                            exc.unidad = pat['datosOrigen']['unidad']
                            exc.sector = pat['datosOrigen']['sector']
                            exc.patrimonioMueble = mueble
                            exc.save()

                        paleo = PatrimonioPaleontologico()
                        paleo.nombreCientifico = pat['datosIdentificacion']['nombreCientifico']
                        paleo.reino = pat['datosIdentificacion']['reino']
                        paleo.phylumDivision = pat['datosIdentificacion']['phylumDivision']
                        paleo.clase = pat['datosIdentificacion']['clase']
                        paleo.eraGeologica = pat['datosIdentificacion']['eraGeologica']
                        paleo.epocaGeologica = pat['datosIdentificacion']['epocaGeologica']
                        paleo.tipoFosilizacion = pat['datosTecnicos']['tipoFosilizacion']
                        paleo.tipoMuestra = pat['datosTecnicos']['tipoMuestra']
                        paleo.patrimonioMueble = mueble
                        paleo.save()

                    elif cat.pk == 10:

                        patrimonio.nombreTituloDemoninacion = pat['datosIdentificacion']['tituloDenominacion']
                        patrimonio.save()

                        if pat['datosOrigen']['excavacion']:
                            exc = Excavacion()
                            exc.areaGeografica = pat['datosOrigen']['areaGeografica']
                            exc.clasificacionOrigen = pat['datosOrigen']['clasificacionOrigen']
                            exc.nombreClasificacion = pat['datosOrigen']['nombreClasificacionOrigen']
                            exc.capa = pat['datosOrigen']['capa']
                            exc.unidad = pat['datosOrigen']['unidad']
                            exc.sector = pat['datosOrigen']['sector']
                            exc.patrimonioMueble = mueble
                            exc.save()

                        if pat['presentaElementosAdicionales']:
                            for elemento in pat['elementosAdicionales']:
                                ele = ElementoAdicional()
                                ele.descripcion = elemento['elemento']
                                ele.material = elemento['material']
                                ele.integridad = elemento['integridadBien']
                                ele.conservacion = elemento['conservacionBien']
                                ele.alto = elemento['alto']
                                ele.largo = elemento['largo']
                                ele.ancho = elemento['ancho']
                                ele.espesor = elemento['espesor']
                                ele.fondo = elemento['fondo']
                                ele.diametro = elemento['diametro']
                                ele.patrimonioMueble = mueble
                                ele.save()

                        for material in pat['datosTecnicos']['materialesSecundarios']:
                            mat = MaterialSecundario.objects.filter(descripcion=material)
                            if len(mat) > 0:
                                mat = MaterialSecundario.objects.get(descripcion=material)
                            else:
                                mat = MaterialSecundario()
                                mat.descripcion = material
                                mat.save()
                            mueble.materialesSecundarios.add(mat)

                        for tecnica in pat['datosTecnicos']['tecnicasManufactura']:
                            tec = TecnicaManufactura.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaManufactura.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaManufactura()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasManifactura.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasDecoracion']:
                            tec = TecnicaDecoracion.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaDecoracion.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaDecoracion()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasDecoracion.add(tec)

                        for tecnica in pat['datosTecnicos']['tecnicasAcabado']:
                            tec = TecnicaAcabado.objects.filter(descripcion=tecnica)
                            if len(tec) > 0:
                                tec = TecnicaAcabado.objects.get(descripcion=tecnica)
                            else:
                                tec = TecnicaAcabado()
                                tec.descripcion = tecnica
                                tec.save()
                            mueble.tecnicasAcabado.add(tec)
                        mueble.save()

                        indus = PatrimonioIndustrial()
                        indus.modeloMarca = pat['datosIdentificacion']['modeloMarca']
                        indus.serie = pat['datosIdentificacion']['serie']
                        indus.procedencia = pat['datosIdentificacion']['procedencia']
                        indus.datacion = pat['datosIdentificacion']['datacion']
                        indus.materialSoporte = pat['datosTecnicos']['materialSoporte']
                        indus.fondo = pat['datosTecnicos']['dimensionesYPeso']['fondo']
                        indus.diametro = pat['datosTecnicos']['dimensionesYPeso']['diametro']
                        indus.patrimonioMueble = mueble
                        indus.save()

                        for fabricante in pat['datosIdentificacion']['fabricante']:
                            fab = Fabricante.objects.filter(nombre=fabricante)
                            if len(fab) > 0:
                                fab = Fabricante.objects.get(nombre=fabricante)
                            else:
                                fab = Fabricante()
                                fab.nombre = fabricante
                                fab.save()
                            indus.fabricantes.add(fab)
                        indus.save()

    patrimonios = Patrimonio.objects.filter(estado=1).order_by('nombreTituloDemoninacion')

    context = {
        'patrimonios': patrimonios,
        'cantidad': len(patrimonios),
    }

    return render(request, 'patrimonio/patrimony_list.html', context=context)

@api_view(('GET',))
def instituciones_list_api(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page - 1) * length
    end = start + length
    queryset = Institucion.objects.filter(nombre__icontains=search,estado='1').order_by('nombre')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = InstitucionSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

@api_view(('GET',))
def gestorPatrimonio_list_api(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page - 1) * length
    end = start + length
    queryset = User.objects.filter(first_name__icontains=search).order_by('first_name')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = UserSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

def patrimonio_edit(request,pk):
    patrimonio = -1
    #patrimonio = Patrimonio.objects.get(pk=pk)
    entradas = Entrada.objects.filter()
    actividadesTuristicas = ActividadTuristica.objects.filter()
    if int(pk) == 1:
        categorias = Categoria.objects.filter(tipo=2)
        context = {
            'patrimonio': patrimonio,
            'categorias': categorias,

        }
        return render(request, 'patrimonio/patrimony_inmueble_edit.html', context)
    else:
        categorias = Categoria.objects.filter(tipo=1)
        tiposIngreso = PatrimonioInMaterial.tipoIngreso.field.choices
        context = {
            'patrimonio': patrimonio,
            'categorias': categorias,
            'tiposIngreso': tiposIngreso,
            'entradas': entradas,
            'actividades_turisticas': actividadesTuristicas,
        }
        return render(request, 'patrimonio/patrimony_inmaterial_edit.html', context)

def detalle(request, pk):
    valor = Patrimonio.objects.get(pk=pk)
    zona = PuntoGeografico.objects.get(patrimonio_id=pk)
    valoraciones = PatrimonioValoracion.objects.filter(zona=zona).filter(estado=2)
    puntuacion=0
    for v in valoraciones:
        puntuacion = v.valoracion + puntuacion
    if len(valoraciones):
        puntuacion=puntuacion/len(valoraciones)
    context = {'puntacion': puntuacion, 'valor': valor, 'valoraciones': valoraciones,
               'afectaciones': [c[1] for c in Incidente.AFECTACION]}

    if request.POST.get("accion") == "incidente":
        print(request.POST)
        incidente = Incidente.objects.create()
        zona = PuntoGeografico.objects.get(patrimonio_id=pk)
        for c in Incidente.AFECTACION:
            if c[1] == request.POST.get("tipo"):
                incidente.tipoAfectacion = c[0]
                break
        incidente.fechaOcurrencia = request.POST.get("fecha")
        incidente.descripcion = request.POST.get("descripcion")
        incidente.nombre = request.POST.get("nombre")
        incidente.correo = request.POST.get("email")
        incidente.telefono = request.POST.get("telefono")
        incidente.zona_id = zona.id
        #zona=PuntoGeografico.objects.get(patrimonio_id=pk)
        incidente.codigo = "INCD" + str(incidente.id).zfill(6)
        incidente.save()
        return HttpResponseRedirect(reverse(detalle, args=[pk]))

    if request.POST.get("accion_valoracion") == "valoracion":
        print(request.POST)
        valoracion = PatrimonioValoracion.objects.create()
        valoracion.patrimonio_id = pk;
        valoracion.nombre = request.POST.get("name")
        valoracion.correo = request.POST.get("email")
        valoracion.comentario = request.POST.get("comment")
        valoracion.valoracion = request.POST.get("score")
        valoracion.save()
        send_email(request, valoracion.pk)
        return HttpResponseRedirect(reverse(detalle, args=[pk]))
    return render(request, 'patrimonio/templateDetail.html', context)

def detalle_museo(request, pk):
    #Provisional hasta cambio de la bd
    #museo
    valor = {'url': 'https://enlima.pe/sites/default/files/mali-lima.jpg',
             'nombre': 'Museo Nacional de Arqueología, Antropología e Historia del Perú'}

    area = {'direccion': 'Plaza Bolivar s/n',
            'departamento': 'Lima',
            'provincia': 'Lima',
            'distrito': 'Pueblo Libre'}

    institucion = Institucion.objects.get(pk=pk)
    #lista de patrimonio dentro del museo
    patrimonios = Patrimonio.objects.filter(institucion_id=pk)
    #lista de valoraciones general de la institucion
    valoraciones = PatrimonioValoracion.objects.filter(zona__institucion_id=pk).filter(estado=2)
    #lista de incidentes
    incidentes = Incidente.objects.filter(zona__institucion_id=pk)

    context = {"valor": valor,
               "area": area,
               "institucion": institucion,
               "patrimonios": patrimonios,
               "valoraciones": valoraciones,
               "incidentes": incidentes,
               'afectaciones': [c[1] for c in Incidente.AFECTACION]}

    return render(request, 'patrimonio/patrimony_museum.html',context)

def valor_museo(request,pk):
    if request.POST:
        zona = PuntoGeografico.objects.get(institucion_id=pk)
        valoracion = PatrimonioValoracion.objects.create()
        valoracion.zona = zona
        valoracion.nombre = request.POST.get("name")
        valoracion.correo = request.POST.get("email")
        valoracion.comentario = request.POST.get("comment")
        valoracion.valoracion = request.POST.get("score")
        valoracion.save()
        send_email(request, valoracion.pk)
    return HttpResponseRedirect(reverse(detalle_museo, args=[pk]))

def incidete_museo(request,pk):
    if request.POST:
        zona = PuntoGeografico.objects.get(institucion_id=pk)
        incidente = Incidente.objects.create()

        for c in Incidente.AFECTACION:
            if c[1] == request.POST.get("tipo"):
                incidente.tipoAfectacion = c[0]
                break

        incidente.fechaOcurrencia = request.POST.get("fecha")
        incidente.descripcion = request.POST.get("descripcion")
        incidente.nombre = request.POST.get("nombre")
        incidente.correo = request.POST.get("email")
        incidente.telefono = request.POST.get("telefono")
        incidente.zona_id = zona.id
        incidente.codigo = "INCD" + str(incidente.id).zfill(6)
        incidente.save()
    return HttpResponseRedirect(reverse(detalle_museo, args=[pk]))

@method_decorator(csrf_exempt)
def send_email(request, pk):

    if str(ALLOWED_HOSTS) == "[]":
        url = "http://localhost:8000/patrimonios/email_confirmation/" + str(pk)
    else:
        url = "http://119.8.150.164:8080/patrimonios/email_confirmation/" + str(pk)

    if request.POST:
        try:
            subject = "Confirma tu correo electrónico"
            sender = 'info@inova.team'

            #enviar enlace a una vista de confirmacion
            context = {
                'url_val': url
            }
            template = get_template('patrimonio/patrimony_email.html')
            content = template.render(context)

            correos = [request.POST.get("email")]
            for correo in correos:
                correo = correo.strip()
                email = EmailMultiAlternatives(subject, '', sender, [correo], cc=[])
                email.attach_alternative(content, 'text/html')
                email.send()
            print('Se envió el correo con éxito')
        except Exception as e:
            print(str(e))

def email_confirmation(request, pk):
    valor = PatrimonioValoracion.objects.get(pk=pk)
    valor.estado = 2
    valor.save()
    context = {'valor':valor}
    return render(request, 'patrimonio/email_confirmation.html', context)
