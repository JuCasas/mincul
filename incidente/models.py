from django.db import models

#Create your models here.
from patrimonios.models import Patrimonio, Institucion, PuntoGeografico
from mincul_app.models import Documento


class Incidente(models.Model):
    ESTADOS = [
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    ]
    AFECTACION = (
        ('1', 'Invasión/Ocupación Ilegal/Ampliación de Invasión'),
        ('2', 'Deterioro de patrimonio por efectos de la persona'),
        ('3','Deterioro de patrimonio por efectos de la naturaleza'),
        ('4','Destrucción en zonas arqueológicas'),
        ('5','Destrucción de casonas'),
        ('6','Huaquería'),
        ('7','Otros'),
    )
    STATUS = (
        ('1', 'Registrado'),
        ('2', 'En Proceso'),
        ('3', 'Resuelto'),
        ('4', 'Denegado'),
    )
    codigo = models.CharField(max_length=10, null=True)
    tipoAfectacion = models.CharField(max_length=2, choices=AFECTACION, default='1', null=True, blank=True)
    fechaOcurrencia = models.DateField(blank=True, null=True, verbose_name='fechaOcurrencia')
    descripcion = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=20, null=True)
    fechaRegistro = models.DateField(blank=True, null=True, verbose_name='fechaRegistro')
    fechaAprobacion = models.DateField(blank=True, null=True, verbose_name='fechaAprobacion')
    zona = models.ForeignKey(PuntoGeografico, on_delete=models.CASCADE, null=True)
    documentos = models.ManyToManyField(Documento)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default='1', null=True, blank=True)

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
