from rest_framework import serializers
from incidente.models import Incidente
from patrimonios.models import PuntoGeografico


class IncidenteSerializer(serializers.ModelSerializer):
    fechaRegistro = serializers.DateField(format='%d/%m/%Y', required=False)
    zona = serializers.SerializerMethodField()

    class Meta:
        model = Incidente
        fields = ['id','codigo','nombre','correo','telefono','descripcion','zona','tipoAfectacion','fechaRegistro','status']

    def get_zona(self, obj):
        return obj.zona.nombre

class PuntoGeograficoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PuntoGeografico
        fields = ['id','nombre']