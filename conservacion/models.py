from django.db import models

# Create your models here.
from mincul import settings
from patrimonios.models import Patrimonio
from mincul_app.models import Documento
from incidente.models import Incidente

class ProyectoConservacion(models.Model):
    ORDER_COLUMN_CHOICES = {
        '0': 'codigo',
        '1': 'nombre',
        '2': 'tipoProyecto',
        '3': 'cantidadAct',
        '4': 'fechaInicio',
        '5': 'status'
    }

    TIPOS = (
        ('0','Preventivo'),
        ('1','Correctivo'),
        ('2', 'Curativo'),
    )
    ESTADOS = (
        ('1','Activo'),
        ('2','Inactivo'),
    )
    STATUS = (
        ('0', 'En Proceso'),
        ('1','Registrado'),
        ('2','Completado'),
    )
    codigo = models.CharField(max_length=10, null=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField(blank=True, null=True, verbose_name='fechaInicio')
    fechaFin = models.DateField(blank=True, null=True, verbose_name='fechaFin')
    tipoProyecto = models.CharField(max_length=2,choices=TIPOS,default='0',null=True,blank=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    cantidadAct = models.IntegerField(default=0,blank=True,null=True)
    cantidadActR = models.IntegerField(default=0,blank=True,null=True)
    documentos = models.ManyToManyField(Documento)
    patrimonios = models.ManyToManyField(Patrimonio)
    incidentes = models.ManyToManyField(Incidente)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default='1', null=True, blank=True)

class Actividad(models.Model):
    ORDER_COLUMN_CHOICES = {
        '0': 'codigo',
        '1': 'nombre',
        '2': '',
        '3': 'patrimonio__nombreTituloDemoninacion',
        '4': 'fechaInicio',
        '5': 'fechaFin',
        '6': 'status'
    }

    STATUS = (
        ('0', 'En Proceso'),
        ('1','Registrado'),
        ('2','Completado'),
    )
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=50)
    fechaInicio = models.DateField(blank=True, null=True, verbose_name='fechaInicio')
    fechaFin = models.DateField(blank=True, null=True, verbose_name='fechaFin')
    descripcion = models.CharField(max_length=200,blank=True, null=True)
    presupuesto = models.FloatField()
    gastoTotal = models.FloatField()
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(ProyectoConservacion, on_delete=models.CASCADE)
    relaciones = models.ManyToManyField("self", blank=True)
    documentos = models.ManyToManyField(Documento)
    conservadores = models.ManyToManyField(settings.AUTH_USER_MODEL)
    estado = models.CharField(max_length=2,choices=ESTADOS,default='1',null=True,blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default='0', null=True, blank=True)


class Tarea(models.Model):
    ESTADOS = (
        ('1', 'Registrada'),
        ('2', 'En proceso'),
        ('3', 'Finalizada'),
    )
    codigo = models.CharField(max_length=8, null=True)
    nombre = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=200)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    gasto = models.FloatField(blank=True, null=True)
    presupuesto = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True, verbose_name='fecha')
    fechaRegistro = models.DateField(blank=True, null=True, verbose_name='fechaRegistro')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class Campo(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    nombre = models.CharField(max_length=200)
    contenido = models.CharField(max_length=200, null=True, blank=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    documentos = models.ManyToManyField(Documento)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
