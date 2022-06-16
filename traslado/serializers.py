from rest_framework import serializers
from traslado.models import SolicitudTraslado


class TrasladoSerializer(serializers.ModelSerializer):

    fechaSalidaProgramada = serializers.DateField(format='%d/%m/%Y', required=False)
    fechaRetornoProgramada = serializers.DateField(format='%d/%m/%Y', required=False)
    entidadSolicitante = serializers.CharField(source='entidadSolicitante.nombreSolicitante')
    gestorConservacionTraslados = serializers.CharField(source='gestorConservacionTraslados.username')
    class Meta:
        model = SolicitudTraslado
        fields = ['id','entidadSolicitante','gestorConservacionTraslados','fechaRetornoProgramada','fechaSalidaProgramada','estado']
