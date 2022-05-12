from datetime import datetime

from django.db import models


class DatosProcedencia (models.Model):
    areaGeografica = models.CharField(max_length=30)
    denominacion = models.CharField(max_length=30)
    excavacion = models.IntegerField(null=True)


class DatosPropiedad (models.Model):
    formaAdquisicion = models.CharField(max_length=30)
    propietario = models.CharField(max_length=30)
    tipoDocumento = models.CharField(max_length=30)
    numeroDocumento = models.CharField(max_length=30)


class DatosLocalizacion (models.Model):
    #localizacion: latidud / longitud ¿?
    latitud = models.DecimalField(max_digits=8, decimal_places=3)
    longitud = models.DecimalField(max_digits=8, decimal_places=3)
    direccion = models.CharField(max_length=30)


class DatosConservacion (models.Model):
    estadoConservacion = models.CharField(max_length=30)
    estadoIntegridad = models.CharField(max_length=30)
    detalle = models.CharField(max_length=30)
    tratamiento = models.CharField(max_length=30)


class Dimensiones (models.Model):
    alto = models.DecimalField(max_digits=5, decimal_places=2)
    largo = models.DecimalField(max_digits=5, decimal_places=2)
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    espesor = models.DecimalField(max_digits=5, decimal_places=2)
    fondo = models.DecimalField(max_digits=5, decimal_places=2)
    diametro = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=2)


class DatosTecnicos (models.Model):
    materialPrincipal = models.CharField(max_length=30)
    materialSecundario = models.CharField(max_length=30)
    tManufactura = models.CharField(max_length=30)
    tDecoracion = models.CharField(max_length=30)
    tAcabado = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=30)
    dimensiones = models.OneToOneField(Dimensiones, null=True, on_delete=models.SET_NULL, verbose_name='Dimensiones Patrimonio Cultural')


class EstablecimientoCultural (models.Model):
    descripcion = models.CharField(max_length=30)
    # localizacion: latidud / longitud ¿?
    latitud = models.DecimalField(max_digits=8, decimal_places=3)
    longitud = models.DecimalField(max_digits=8, decimal_places=3)
    direccion = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)


class PatrimonioCultural (models.Model):
    ESTADOS = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )

    clasificacion = models.CharField(max_length=30)
    tipoBien = models.CharField(max_length=30)
    demoninacion = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    autoria = models.IntegerField(null=True)
    lugarManufactura = models.CharField(max_length=30)
    estilo = models.CharField(max_length=30)
    datacion = models.DateField(default=datetime.now, blank=True, null=True, verbose_name='Datación')
    valorCultural = models.CharField(max_length=30)
    otrosCodigos = models.CharField(max_length=30)
    observaciones = models.CharField(max_length=30)
    posicion = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='1')
    datosProcedencia = models.OneToOneField(DatosProcedencia, null=True, on_delete=models.SET_NULL, verbose_name='Datos de Procedencia')
    datosPropiedad = models.OneToOneField(DatosPropiedad, null=True, on_delete=models.SET_NULL, verbose_name='Datos de Propiedad')
    datosLocalizacion = models.OneToOneField(DatosLocalizacion, null=True, on_delete=models.SET_NULL, verbose_name='Datos de Localización')
    datosConservacion = models.OneToOneField(DatosConservacion, null=True, on_delete=models.SET_NULL, verbose_name='Datos de Conservación')
    datosTecnicos = models.OneToOneField(DatosTecnicos, null=True, on_delete=models.SET_NULL, verbose_name='Datos Técnicos')
    establecimientoCultural = models.ForeignKey(EstablecimientoCultural, null=True, on_delete=models.SET_NULL, verbose_name='Establecimiento Cultural')


class ElementoAdicional (models.Model):
    material = models.CharField(max_length=30)
    integridad = models.CharField(max_length=30)
    conservacion = models.CharField(max_length=30)
    patrimonioCultural = models.ForeignKey(PatrimonioCultural, null=True, on_delete=models.SET_NULL, verbose_name='Patrimonio Cultural')
    dimensiones = models.OneToOneField(Dimensiones, null=True, on_delete=models.SET_NULL, verbose_name='Dimensiones Elemento Adicional')