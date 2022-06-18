from django.db import models

#Create your models here.
from patrimonios.models import Patrimonio
from mincul_app.models import Documento


class Incidente(models.Model):
    ESTADOS = [
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    ]
    AFECTACION = [
        ('0', 'Leve'),
        ('1', 'Urgente'),
    ]
    TIPOINCIDENTADO = [
        ('1', 'Patrimonio'),
        ('2', 'Institucion'),
    ]
    tipoAfectacion = models.CharField(max_length=2, choices=AFECTACION, default='1', null=True, blank=True)
    fechaOcurrencia = models.DateField(blank=True, null=True, verbose_name='fechaOcurrencia')
    descripcion = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=20, null=True)
    fechaRegistro = models.DateField(blank=True, null=True, verbose_name='fechaRegistro')
    fechaAprobacion = models.DateField(blank=True, null=True, verbose_name='fechaAprobacion')
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE, null=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True)
    tipoIncidentado = models.CharField(max_length=2, choices=TIPOINCIDENTADO, default='1', null=True, blank=True)
    documentos = models.ManyToManyField(Documento)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class Valoracion(models.Model):
    ESTADOS = [
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
    valoracion = models.IntegerField()
    comentario = models.CharField(max_length=200)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
