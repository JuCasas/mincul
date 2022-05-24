from django.db import models

# Create your models here.
from conservacion.models import Documento
from mincul import settings
from patrimonios.models import Patrimonio


class SolicitudTraslado(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    doiSolicitante = models.CharField(max_length=12, null=True, blank=True)
    nombreSolicitante = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    #TODO: ubigeoSolicitante
    telefonoSolicitante  = models.CharField(max_length=9, null=True, blank=True)
    celularSolicitante = models.CharField(max_length=9, null=True, blank=True)
    correoSolicitante = models.CharField(max_length=100, null=True, blank=True)
    representanteLegal = models.CharField(max_length=100, null=True, blank=True)
    doiRepresentante = models.CharField(max_length=12, null=True, blank=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    nombreResponsable = models.CharField(max_length=200, null=True, blank=True)
    numeroRNAoRNDA = models.CharField(max_length=20, null=True, blank=True)
    domicilioResponsable = models.CharField(max_length=200, null=True, blank=True)
    procedenciaMuestras = models.CharField(max_length=200, null=True, blank=True)
    personaEfectuaraTraslado = models.CharField(max_length=200, null=True, blank=True)
    destino = models.CharField(max_length=200, null=True, blank=True)
    # TODO: ubigeoDestino
    fechaSalidaProgramada = models.DateField(blank=True, null=True, verbose_name='fechaSalidaProgramada')
    fechaRetornoProgramada =models.DateField(blank=True, null=True, verbose_name='fechaRetornoProgramada')
    fechaSalidaReal = models.DateField(blank=True, null=True, verbose_name='fechaSalidaReal')
    fechaRetornoReal = models.DateField(blank=True, null=True, verbose_name='fechaRetornoReal')
    # TODO: tipoPersona
    gestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='gestor')
    gestorConservacionTraslados = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='gestorConservacionTraslados')
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
    patrimonios = models.ManyToManyField(Patrimonio)
    documentos = models.ManyToManyField(Documento)

class SolicitudPorPatrimonio(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    solicitud = models.ForeignKey(SolicitudTraslado, on_delete=models.CASCADE)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

class DocumentoPorSolicitud(models.Model):
    TIPOS = (
        ('0', 'Documento'),
        ('1', 'Declaracion Jurada'),
    )
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    documento =  models.ForeignKey(Documento, on_delete=models.CASCADE)
    solicitud =  models.ForeignKey(SolicitudTraslado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPOS, default='1', null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
