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
    nombre = models.CharField(max_length=200)
    doi = models.CharField(max_length=12, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=9, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
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
    institucion = models.ForeignKey(Institucion,null=True, on_delete=models.CASCADE)
    propietarios = models.ManyToManyField(Propietario)


class PropietarioPorPatrimonio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    Patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class Servicio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class ActividadTuristica(models.Model):
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
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')
    tipo = models.CharField(max_length=2, choices=TIPO, default='1')

class Entrada(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')


class PatrimonioMaterial(models.Model):
    horaApertura = models.TimeField(auto_now_add=True, blank=True)
    horaCierre = models.TimeField(auto_now_add=True, blank=True)
    patrimonio = models.OneToOneField(Patrimonio, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    actividades = models.ManyToManyField(ActividadTuristica)
    entradas = models.ManyToManyField(Entrada)


class EntradaPorPatrimonio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    patrimonio = models.ForeignKey(PatrimonioMaterial, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class ActividadTuristicaPorPatrimonio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    actividadTuristica = models.ForeignKey(ActividadTuristica, on_delete=models.CASCADE)
    patrimonio = models.ForeignKey(PatrimonioMaterial, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class ServicioPorPatrimonio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    patrimonio = models.ForeignKey(PatrimonioMaterial, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1')

class PatrimonioMaterialMueble(models.Model):
    alto = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2)
    largo = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2)
    ancho = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2)
    patrimoniomaterial = models.ForeignKey(PatrimonioMaterial, on_delete=models.CASCADE)