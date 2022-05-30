from django.contrib import admin
from patrimonios.models import Institucion, Patrimonio, Propietario
from traslado.models import EntidadSolicitante

# Register your models here.

admin.site.register(Institucion)
admin.site.register(Patrimonio)
admin.site.register(Propietario)
admin.site.register(EntidadSolicitante)