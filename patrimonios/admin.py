from django.contrib import admin
from patrimonios.models import Institucion, Patrimonio, Propietario

# Register your models here.

admin.site.register(Institucion)
admin.site.register(Patrimonio)
admin.site.register(Propietario)