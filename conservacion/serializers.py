from rest_framework import serializers
from conservacion.models import ProyectoConservacion, Tarea
from conservacion.models import Actividad
from patrimonios.models import Patrimonio
from authentication.models import User


class ProyectoConservacionSerializer(serializers.ModelSerializer):

    fechaInicio = serializers.DateField(format='%d/%m/%Y', required=False)
    fechaFin = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = ProyectoConservacion
        fields = ['id','codigo','nombre','descripcion','fechaInicio','fechaFin','tipoProyecto','status','cantidadAct','cantidadActR']

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

class ConservadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'codigo', 'first_name', 'last_name']

class RelacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actividad
        fields = ['id','codigo','nombre']

class ActividadSerializer (serializers.ModelSerializer):

    fechaFin = serializers.DateField(format='%d/%m/%Y', required=False)
    patrimonio = serializers.CharField(source='patrimonio.nombreTituloDemoninacion')
    patrimonioPk = serializers.IntegerField(source='patrimonio.pk')
    conservadores = ConservadorSerializer(read_only=True, many=True)
    relaciones = RelacionSerializer(read_only=True, many=True)
    total_conservadores = serializers.SerializerMethodField()
    fechaInicio = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = Actividad
        fields = ['patrimonioPk','id','codigo','nombre','fechaInicio','fechaFin','presupuesto','gastoTotal','estado','descripcion','status', "patrimonio", "total_conservadores","relaciones","conservadores"]

    def get_total_conservadores(self, instance):
        return instance.conservadores.count()