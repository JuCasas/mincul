from rest_framework import serializers
from conservacion.models import ProyectoConservacion


class ProyectoConservacionSerializer(serializers.ModelSerializer):

    fechaInicio = serializers.DateField(format='%d/%m/%Y', required=False)
    fechaFin = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = ProyectoConservacion
        fields = ['id','codigo','nombre','descripcion','fechaInicio','fechaFin']
