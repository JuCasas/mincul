from django.db import models

# Create your models here.
# from incidente.models import Incidente
from mincul import settings
from patrimonios.models import Patrimonio


class ProyectoConservacion(models.Model):
    TIPOS = [
        ('0','Preventivo'),
        ('1','Correctivo'),
    ]
    ESTADOS = [
        ('1','Activo'),
        ('2','Inactivo'),
    ]
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField(blank=True, null=True, verbose_name='fechaInicio')
    fechaFin = models.DateField(blank=True, null=True, verbose_name='fechaFin')
    tipoProyecto = models.CharField(max_length=2,choices=TIPOS,default='0',null=True,blank=True)
    estado = models.CharField(max_length=2,choices=ESTADOS,default='1',null=True,blank=True)
    patrimonios = models.ManyToManyField(Patrimonio)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    # incidentes  = models.ManyToManyField(Incidente)

class Documento(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    url = models.CharField(max_length=300,null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)


class Actividad(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=50)
    fechaInicio = models.DateField(blank=True, null=True, verbose_name='fechaInicio')
    fechaFin = models.DateField(blank=True, null=True, verbose_name='fechaFin')
    presupuesto = models.FloatField()
    gastoTotal = models.FloatField()
    patrimonio = models.ForeignKey(ProyectoConservacion, on_delete=models.CASCADE)
    documentos = models.ManyToManyField(Documento)
    #TODO: Definir field actividadPrevia
    estado = models.CharField(max_length=2,choices=ESTADOS,default='1',null=True,blank=True)
    conservadores = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Tarea(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    descripcion = models.CharField(max_length=200)
    materiales = models.CharField(max_length=200, null=True, blank=True)
    herramientas =models.CharField(max_length=200, null=True, blank=True)
    indumentaria =models.CharField(max_length=200, null=True, blank=True)
    gasto = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True, verbose_name='fecha')
    fechaRegistro = models.DateField(blank=True, null=True, verbose_name='fechaRegistro')
    conservador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    documentos = models.ManyToManyField(Documento)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class DocumentoPorTarea(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    tarea = models.ForeignKey(Tarea,on_delete=models.CASCADE )
    documento = models.ForeignKey(Documento,on_delete=models.CASCADE )
    campo = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

    # class Meta:
    #     unique_together = [['tarea','documento']]

class CampoExtra(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    nombre = models.CharField(max_length=200)
    contenido = models.CharField(max_length=200, null=True, blank=True)
    tarea = models.ForeignKey(Tarea,on_delete=models.CASCADE )
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class DocumentoPorActividad(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    actvidad = models.ForeignKey(Actividad,on_delete=models.CASCADE )
    documento = models.ForeignKey(Documento,on_delete=models.CASCADE )
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)



class ConservadorPorActividad(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    conservador = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE )
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE )
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class PatrimonioPorProyecto(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    patrimonio = models.ForeignKey(Patrimonio,on_delete=models.CASCADE )
    proyecto = models.ForeignKey(ProyectoConservacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)


