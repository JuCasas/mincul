from django.db import models

# Create your models here.
from mincul import settings
from patrimonios.models import Patrimonio


class ProyectoConservacion(models.Model):
    ESTADOS = [
        ('1','Preventivo'),
        ('2','Correctivo'),
    ]
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField(blank=True, null=True, verbose_name='fechaInicio')
    fechaFin = models.DateField(blank=True, null=True, verbose_name='fechaFin')
    tipoProyecto = models.CharField(max_length=50)
    estado = models.CharField(max_length=2,choices=ESTADOS,default='1',null=True,blank=True)
    patrimonios = models.ManyToManyField(Patrimonio)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)