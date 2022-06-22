from rest_framework import serializers
from incidente.models import Incidente



class IncidenteSerializer(serializers.ModelSerializer):
    fechaRegistro = serializers.DateField(format='%d/%m/%Y', required=False)
    zona = serializers.SerializerMethodField()

    class Meta:
        model = Incidente
        fields = ['id','codigo','nombre','zona','tipoAfectacion','fechaRegistro','status']

    def get_zona(self, obj):
            return obj.zona.id

