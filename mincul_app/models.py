import unicodedata

from django.db import models

# Create your models here.

import os

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Create your models here.
def substring_after(s, delim):
    return s.rpartition(delim)[-1]

def upload_location_archive(instance, filename):
    extension = substring_after(filename, '.')
    return 'archive/%s.%s' % (remove_accents(instance.horario.codigo), extension)

class Documento(models.Model):
    ESTADOS = (
        ('1', 'Activo'),
        ('2', 'Inactivo'),
    )
    url = models.FileField(max_length=300,null=True, blank=True, upload_to='archive/')
    estado = models.CharField(max_length=2, choices=ESTADOS, default='1', null=True, blank=True)

    def filename(self):
        return os.path.basename(self.url.name)