from rest_framework import serializers
from conservacion.models import ProyectoConservacion
from conservacion.models import Actividad



class ProyectoConservacionSerializer(serializers.ModelSerializer):

    fechaInicio = serializers.DateField(format='%d/%m/%Y', required=False)
    fechaFin = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = ProyectoConservacion
        fields = ['id','codigo','nombre','descripcion','fechaInicio','fechaFin','tipoProyecto','status','cantidadAct','cantidadActR']


class ActividadSerializer (serializers.ModelSerializer):

    fechaInicio = serializers.DateField(format='%d/%m/%Y', required=False)
    fechaFin = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = Actividad
        fields = ['id','codigo','nombre','descripcion','fechaInicio','fechaFin','status']
