from django.db import models

# Create your models here.
# from conservacion.models import Documento, ProyectoConservacion
# from patrimonios.models import Patrimonio


# class Incidente(models.Model):
#     ESTADOS = (
#         ('1', 'Activo'),
#         ('2', 'Inactivo'),
#     )
#     PRIORIDAD = (
#         ('0', 'Leve'),
#         ('1', 'Urgente'),
#     )
#     fechaRegistro = models.DateField(blank=True, null=True, verbose_name='fechaRegistro')
#     fechaAprobacion = models.DateField(blank=True, null=True, verbose_name='fechaAprobacion')
#     prioridad = models.CharField(max_length=2, choices=PRIORIDAD, default='1', null=True, blank=True)
#     patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE)
#     documento =  models.ForeignKey(Documento, on_delete=models.CASCADE)
#     estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)
#
# class IncidentePorProyecto(models.Model):
#     ESTADOS = (
#         ('1', 'Activo'),
#         ('2', 'Inactivo'),
#     )
#     incidente = models.ForeignKey(Incidente,on_delete=models.CASCADE )
#     proyecto = models.ForeignKey(ProyectoConservacion,on_delete=models.CASCADE )
#     estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)