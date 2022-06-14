from django.db import models

# Create your models here.
from mincul import settings
from patrimonios.models import Patrimonio
from mincul_app.models import Documento


class EntidadSolicitante(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    TIPOS = (
        ('0', 'Tipo1'),
        ('1', 'Tipo2'),
    )
    doiSolicitante = models.CharField(max_length=12, null=True, blank=True)
    nombreSolicitante = models.CharField(max_length=200, null=True, blank=True)
    correo = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    tipo = models.CharField(max_length=2, choices=TIPOS, default='1', null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class SolicitudTraslado(models.Model):
    ESTADOS = (
        ('1', 'Registrada'),
        ('2', 'En evaluación'),
        ('3', 'Rechazada'),
        ('4', 'Aprobada'),
        ('5', 'Ejecutada'),
    )
    TIPOS = (
        ('0', 'Tipo1'),
        ('1', 'Tipo2'),
    )
    nombreExposicion = models.CharField(max_length=200, null=True, blank=True)
    destino = models.CharField(max_length=200, null=True, blank=True)
    pais = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    numeroResolucion = models.CharField(max_length=200, null=True, blank=True)
    fechaSalidaProgramada = models.DateField(blank=True, null=True, verbose_name='fechaSalidaProgramada')
    fechaRetornoProgramada = models.DateField(blank=True, null=True, verbose_name='fechaRetornoProgramada')
    fechaSalidaReal = models.DateField(blank=True, null=True, verbose_name='fechaSalidaReal')
    fechaRetornoReal = models.DateField(blank=True, null=True, verbose_name='fechaRetornoReal')
    ubigeoDestino = models.IntegerField(blank=True, null=True)
    tipoTraslado = models.CharField(max_length=2, choices=TIPOS, default='1', null=True, blank=True)
    gestorPatrimonio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='gestorPatrimonioTraslado')
    gestorConservacionTraslados = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                                    related_name='gestorConservacionTrasladosTraslado')
    entidadSolicitante = models.ForeignKey(EntidadSolicitante, on_delete=models.CASCADE)
    patrimonios = models.ManyToManyField(Patrimonio)
    documentos = models.ManyToManyField(Documento, through='DocumentoPorSolicitud')
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
    detalleRechazo = models.CharField(max_length=250, null=True, blank=True)

class DocumentoPorSolicitud(models.Model):
    TIPOS = (
        ('0', 'Documento'),
        ('1', 'Declaracion Jurada'),
    )
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(SolicitudTraslado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPOS, default='1', null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
