from datetime import datetime

from django.db import models
from mincul import settings
from mincul_app.models import Documento


class Institucion(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class Propietario(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    nombre = models.CharField(max_length=200)
    doi = models.CharField(max_length=12, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=9, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')
    documentos = models.ManyToManyField(Documento)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class Autor(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class Responsable(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    institucion = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=9, null=True, blank=True)
    fecha = models.DateField(blank=True, null=True, verbose_name='fecha')
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class Patrimonio (models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )

    TIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )

    CATEGORIA = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )

    nombreTituloDemoninacion = models.CharField(max_length=30)
    # datacion = models.DateField(default=datetime.now, blank=True, null=True, verbose_name='datacion')
    codigo = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    # ubicacion = models.PointField(geography=True, default=Point(0.0, 0.0))
    # https: // raphael - leger.medium.com / django - handle - latitude - and -longitude - 54
    # a4bb2f6e3b
    descripcion = models.CharField(max_length=200)
    observacion = models.CharField(max_length=200)
    tipoPatrimonio = models.CharField(max_length=2, choices=TIPO, default='1')
    categoria = models.CharField(max_length=2, choices=CATEGORIA, default='1')
    institucion = models.ForeignKey(Institucion,null=True, on_delete=models.CASCADE)
    gestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    propietarios = models.ManyToManyField(Propietario)
    responsables = models.ManyToManyField(Responsable)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')
    pronombre = models.CharField(max_length=1, null=True, blank=True)
    url = models.CharField(max_length=1024, null=True, blank=True)

class Servicio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )

    CATEGORIA = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    categoria = models.CharField(max_length=2, choices=CATEGORIA, default='1')
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')
    observacion = models.CharField(max_length=200)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class ActividadTuristica(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPO = (
        ('1', 'Tipo 1'),
        ('2', 'Tipo 2'),
        ('3', 'Tipo 3'),
        ('4', 'Tipo 4'),
    )

    CATEGORIA = (
        ('1', 'Categoría 1'),
        ('2', 'Categoría 2 '),
        ('3', 'Categoría 3'),
        ('4', 'Categoría 4'),
    )
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.CharField(max_length=2, choices=CATEGORIA, default='1')
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')
    observacion = models.CharField(max_length=200, null=True, blank=True)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class Entrada(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    precio = models.FloatField(blank=True, null=True)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class FuenteBibliografica(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    referencia = models.CharField(max_length=100, null=True, blank=True)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class TecnicaDecoracion(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=200,null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class TecnicaManufactura(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class TecnicaAcabado(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class MaterialSecundario(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class PatrimonioMaterialMueble(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2'),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    nroRegistro = models.CharField(max_length=20, null=True)
    asociacion = models.CharField(max_length=200, null=True)
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')
    integridad = models.CharField(max_length=50, null=True)
    conservacion = models.CharField(max_length=50, null=True)
    detalleConservacion = models.CharField(max_length=200, null=True)
    detalleTratamiento = models.CharField(max_length=200, null=True)
    alto = models.FloatField(default=0.0)
    largo = models.FloatField(default=0.0)
    ancho = models.FloatField(default=0.0)
    espesor = models.FloatField(default=0.0)
    formaAdquisicion = models.CharField(max_length=200, null=True)
    ubicacionEspecifica = models.CharField(max_length=200, null=True)
    situacion = models.CharField(max_length=50, null=True)
    codigoPropietario = models.CharField(max_length=20, null=True)
    codigoRegistroAnteriorINC = models.CharField(max_length=20, null=True)
    codigoInventario = models.CharField(max_length=20, null=True)
    otrosCodigos = models.CharField(max_length=200, null=True)
    tecnicasDecoracion = models.ManyToManyField(TecnicaDecoracion)
    tecnicasManifactura = models.ManyToManyField(TecnicaManufactura)
    tecnicasAcabado = models.ManyToManyField(TecnicaAcabado)
    materialesSecundarios = models.ManyToManyField(MaterialSecundario)
    patrimonio = models.OneToOneField(Patrimonio, on_delete=models.CASCADE)

class PatrimonioArqueologico(models.Model):
    material = models.CharField(max_length=100, null=True)
    tipoMaterial = models.CharField(max_length=100, null=True)
    cultura = models.CharField(max_length=50, null=True)
    estilo = models.CharField(max_length=100, null=True)
    periodo = models.CharField(max_length=100, null=True)
    diametroMax = models.FloatField(default=0.0, null=True)
    diametroMin = models.FloatField(default=0.0, null=True)
    diametroBase = models.FloatField(default=0.0, null=True)
    patrimonioMueble = models.OneToOneField(PatrimonioMaterialMueble,on_delete=models.CASCADE)

class PatrimonioHistoricoArtistico(models.Model):
    material = models.CharField(max_length=100, null=True)
    estilo = models.CharField(max_length=100, null=True)
    procedencia = models.CharField(max_length=100, null=True)
    datacion = models.CharField(max_length=100, null=True)
    materialSoporte = models.CharField(max_length=100, null=True)
    fondo = models.FloatField(default=0.0)
    diametro = models.FloatField(default=0.0)
    patrimonioMueble = models.OneToOneField(PatrimonioMaterialMueble, on_delete=models.CASCADE)

class PatrimonioEtnografico(models.Model):
    filacionCultural = models.CharField(max_length=50, null=True)
    procedencia = models.CharField(max_length=50, null=True)
    datacion = models.CharField(max_length=100, null=True)
    materialSoporte = models.CharField(max_length=100, null=True)
    fondo = models.FloatField(default=0.0)
    diametro = models.FloatField(default=0.0)
    patrimonioMueble = models.OneToOneField(PatrimonioMaterialMueble, on_delete=models.CASCADE)

class PatrimonioPaleontologico(models.Model):
    nombreCientifico = models.CharField(max_length=100, null=True)
    reino = models.CharField(max_length=50, null=True)
    phylumDivision = models.CharField(max_length=50, null=True)
    clase = models.CharField(max_length=50, null=True)
    eraGeologica = models.CharField(max_length=50, null=True)
    epocaGeologica = models.CharField(max_length=50, null=True)
    tipoFosilizacion = models.CharField(max_length=50, null=True)
    tipoMuestra = models.CharField(max_length=50, null=True)
    patrimonioMueble = models.OneToOneField(PatrimonioMaterialMueble, on_delete=models.CASCADE)

class PatrimonioIndustrial(models.Model):
    modeloMarca = models.CharField(max_length=50, null=True)
    serie = models.CharField(max_length=50, null=True)
    fabricante = models.CharField(max_length=200, null=True)
    procedencia = models.CharField(max_length=50, null=True)
    datacion = models.CharField(max_length=50, null=True)
    materialSoporte = models.CharField(max_length=100, null=True)
    fondo = models.FloatField(default=0.0)
    diametro = models.FloatField(default=0.0)
    patrimonioMueble = models.OneToOneField(PatrimonioMaterialMueble, on_delete=models.CASCADE)

class Excavacion(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    areaGeografica = models.CharField(max_length=100, null=True)
    clasificacionOrigen = models.CharField(max_length=100, null=True)
    nombreClasificacion = models.CharField(max_length=100, null=True)
    capa = models.CharField(max_length=100, null=True)
    unidad = models.CharField(max_length=100, null=True)
    sector = models.CharField(max_length=100, null=True)
    patrimonioMueble = models.ForeignKey(PatrimonioMaterialMueble, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class ElementoAdicional(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=200, null=True)
    material = models.CharField(max_length=100, null=True)
    integridad = models.CharField(max_length=100, null=True)
    conservacion = models.CharField(max_length=100, null=True)
    alto = models.FloatField(default=0.0)
    largo = models.FloatField(default=0.0)
    ancho = models.FloatField(default=0.0)
    espesor = models.FloatField(default=0.0)
    fondo = models.FloatField(default=0.0)
    diametro = models.FloatField(default=0.0)
    patrimonioMueble = models.ForeignKey(PatrimonioMaterialMueble, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class PatrimonioMaterialInMueble(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2'),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    SUBTIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2'),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    TIPOINGRESO = (
        ('1', 'Gratuito'),
        ('2', 'Pagado'),
        ('3', 'Estado 3'),
        ('4', 'No información'),
    )
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')
    subtipo = models.CharField(max_length=2, choices=SUBTIPO, default='1')
    particularidades = models.CharField(max_length=200, null=True, blank=True)
    tipoIngreso = models.CharField(max_length=2, choices=TIPOINGRESO, default='1')
    estadoActual = models.CharField(max_length=200)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)

class PatrimonioInMaterial(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2'),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    SUBTIPO = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2'),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )
    TIPOINGRESO = (
        ('1', 'Gratuito'),
        ('2', 'Pagado'),
        ('3', 'Estado 3'),
        ('4', 'No información'),
    )
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')
    subtipo = models.CharField(max_length=2, choices=SUBTIPO, default='1')
    particularidades = models.CharField(max_length=200, null=True, blank=True)
    tipoIngreso = models.CharField(max_length=2, choices=TIPOINGRESO, default='1')
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)

class PatrimonioValoracion(models.Model):
    ESTADOS = (
        ('1', 'Pendiente'),
        ('2', 'Aceptado'),
    )
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(default='', max_length=60)
    correo = models.CharField(default='', max_length=60)
    valoracion = models.IntegerField(default=0)
    comentario = models.CharField(default='', max_length=250)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class EpocaVisita(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    epocaPropicia = models.CharField(max_length=100, null=True, blank=True)
    especificacion = models.CharField(max_length=100, null=True, blank=True)
    horaVisita = models.TimeField(auto_now_add=True, blank=True)
    observaciones = models.CharField(max_length=100, null=True, blank=True)
    patrimonioMaterialInMueble = models.ForeignKey(PatrimonioMaterialInMueble, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')


