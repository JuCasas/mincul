from django.db import models

#Create your models here.
from patrimonios.models import Patrimonio
from mincul_app.models import Documento


class Incidente(models.Model):
    ESTADOS = [
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    ]
    PRIORIDAD = [
        ('0', 'Leve'),
        ('1', 'Urgente'),
    ]
    fechaRegistro = models.DateField(blank=True, null=True, verbose_name='fechaRegistro')
    fechaAprobacion = models.DateField(blank=True, null=True, verbose_name='fechaAprobacion')
    prioridad = models.CharField(max_length=2, choices=PRIORIDAD, default='1', null=True, blank=True)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    documento =  models.ForeignKey(Documento, on_delete=models.CASCADE)
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
