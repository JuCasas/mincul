from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from mincul_app.models import Documento


class User(AbstractUser):
    doi = models.CharField(max_length=12)
    celular = models.CharField(max_length=20)
    codigo = models.CharField(max_length=20, null=True)
    foto = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True)