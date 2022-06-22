from rest_framework import serializers
from conservacion.models import ProyectoConservacion, Tarea
from conservacion.models import Actividad
from patrimonios.models import Patrimonio


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
        fields = ['id','codigo','nombre','descripcion','fechaInicio','fechaFin','status', "patrimonio"]

class TareaSerializer (serializers.ModelSerializer):

    fechaRegistro = serializers.DateField(format='%d/%m/%Y', required=False)
    fecha = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = Tarea
        fields = ['id','codigo','nombre','descripcion','fechaRegistro','fecha','presupuesto','gasto']
        #                                               fechaInicio   , fechaFin

class PatrimonioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patrimonio
        fields = ['id','nombreTituloDemoninacion']