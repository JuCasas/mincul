from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    doi = models.CharField(max_length=12)
    celular = models.CharField(max_length=9)
    