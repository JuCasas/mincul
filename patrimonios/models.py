from datetime import datetime

from django.db import models


# class DatosProcedencia (models.Model):
#     areaGeografica = models.CharField(max_length=30)
#     denominacion = models.CharField(max_length=30)
#     excavacion = models.IntegerField(null=True)
#
#
# class DatosPropiedad (models.Model):
#     formaAdquisicion = models.CharField(max_length=30)
#     propietario = models.CharField(max_length=30)
#     tipoDocumento = models.CharField(max_length=30)
#     numeroDocumento = models.CharField(max_length=30)
#
#
# class DatosLocalizacion (models.Model):
#     #localizacion: latidud / longitud ¿?
#     latitud = models.DecimalField(max_digits=8, decimal_places=3)
#     longitud = models.DecimalField(max_digits=8, decimal_places=3)
#     direccion = models.CharField(max_length=30)
#
#
# class DatosConservacion (models.Model):
#     estadoConservacion = models.CharField(max_length=30)
#     estadoIntegridad = models.CharField(max_length=30)
#     detalle = models.CharField(max_length=30)
#     tratamiento = models.CharField(max_length=30)
#
#
# class Dimensiones (models.Model):
#     alto = models.DecimalField(max_digits=5, decimal_places=2)
#     largo = models.DecimalField(max_digits=5, decimal_places=2)
#     ancho = models.DecimalField(max_digits=5, decimal_places=2)
#     espesor = models.DecimalField(max_digits=5, decimal_places=2)
#     fondo = models.DecimalField(max_digits=5, decimal_places=2)
#     diametro = models.DecimalField(max_digits=5, decimal_places=2)
#     peso = models.DecimalField(max_digits=5, decimal_places=2)
#
#
# class DatosTecnicos (models.Model):
#     materialPrincipal = models.CharField(max_length=30)
#     materialSecundario = models.CharField(max_length=30)
#     tManufactura = models.CharField(max_length=30)
#     tDecoracion = models.CharField(max_length=30)
#     tAcabado = models.CharField(max_length=30)
#     descripcion = models.CharField(max_length=30)
#     dimensiones = models.OneToOneField(Dimensiones, null=True, on_delete=models.SET_NULL, verbose_name='Dimensiones Patrimonio Cultural')
#
#
# class EstablecimientoCultural (models.Model):
#     descripcion = models.CharField(max_length=30)
#     # localizacion: latidud / longitud ¿?
#     latitud = models.DecimalField(max_digits=8, decimal_places=3)
#     longitud = models.DecimalField(max_digits=8, decimal_places=3)
#     direccion = models.CharField(max_length=30)
#     tipo = models.CharField(max_length=30)
from mincul import settings


class Patrimonio (models.Model):
    ESTADOS = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
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
    SUBCATEGORIA = (
        ('1', 'Estado 1'),
        ('2', 'Estado 2 '),
        ('3', 'Estado 3'),
        ('4', 'Estado 4'),
    )

    tituloDemoninacion = models.CharField(max_length=30)
    datacion = models.DateField(default=datetime.now, blank=True, null=True, verbose_name='datacion')
    observaciones = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    # ubicacion = models.PointField(geography=True, default=Point(0.0, 0.0))
    # https: // raphael - leger.medium.com / django - handle - latitude - and -longitude - 54
    # a4bb2f6e3b
    tipoPatrimonio = models.CharField(max_length=2, choices=TIPO, default='1')
    categoria = models.CharField(max_length=2, choices=CATEGORIA, default='1')
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIA, default='1')
    gestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

# class ElementoAdicional (models.Model):
#     material = models.CharField(max_length=30)
#     integridad = models.CharField(max_length=30)
#     conservacion = models.CharField(max_length=30)
#     patrimonioCultural = models.ForeignKey(PatrimonioCultural, null=True, on_delete=models.SET_NULL, verbose_name='Patrimonio Cultural')
#     dimensiones = models.OneToOneField(Dimensiones, null=True, on_delete=models.SET_NULL, verbose_name='Dimensiones Elemento Adicional')