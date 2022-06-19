from rest_framework import serializers

from patrimonios.models import Patrimonio
from traslado.models import SolicitudTraslado


class TrasladoSerializer(serializers.ModelSerializer):

    fechaSalidaProgramada = serializers.DateField(format='%d/%m/%Y', required=False)
    fechaRetornoProgramada = serializers.DateField(format='%d/%m/%Y', required=False)
    entidadSolicitante = serializers.CharField(source='entidadSolicitante.nombreSolicitante')
    gestorConservacionTraslados = serializers.SerializerMethodField()

    def get_gestorConservacionTraslados(self, obj):
        return '{} {}'.format(obj.gestorConservacionTraslados.first_name, obj.gestorConservacionTraslados.last_name)

    class Meta:
        model = SolicitudTraslado
        fields = ['numeroResolucion','id','entidadSolicitante','gestorConservacionTraslados','fechaRetornoProgramada','fechaSalidaProgramada','estado']


class PatrimonioSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='categoria.nombre')
    tipoPatrimonio = serializers.CharField(source='get_tipoPatrimonio_display')
    estado = serializers.CharField(source='get_estado_display')

    # tipoPatrimonio = serializers.SerializerMethodField()
    #
    # def get_gestorConservacionTraslados(self, obj):
    #     return '{} {}'.format(obj.gestorConservacionTraslados.first_name, obj.gestorConservacionTraslados.last_name)

    class Meta:
        model = Patrimonio
        fields = ['id','nombreTituloDemoninacion','categoria','tipoPatrimonio', 'estado']


