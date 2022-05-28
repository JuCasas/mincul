from django.db import models

# Create your models here.

class Documento(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    url = models.CharField(max_length=300,null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)