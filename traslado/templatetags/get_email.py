from django import template
from django.shortcuts import redirect

from traslado.models import EntidadSolicitante

register = template.Library()


@register.filter(name='get_email')
def get_email(ent_pk):
    entidad = EntidadSolicitante.objects.get(pk=ent_pk)
    return entidad.correo