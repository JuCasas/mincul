import os
from cgitb import reset

from rest_framework import serializers
from incidente.models import Incidente
from mincul_app.models import Documento
from patrimonios.models import PuntoGeografico

class DocumentoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Documento
        fields = ['id','name','url']
    def get_name(self, instance):
        return os.path.basename(instance.url.name)


class IncidenteSerializer(serializers.ModelSerializer):
    fechaRegistro = serializers.DateField(format='%d/%m/%Y', required=False)
    zona = serializers.SerializerMethodField()
    proyecto = serializers.SerializerMethodField()
    documentos = DocumentoSerializer(read_only=True, many=True)

    class Meta:
        model = Incidente
        fields = ['documentos','id','codigo','nombre','correo','telefono','descripcion','zona','tipoAfectacion','fechaRegistro','status','proyecto']

    def get_zona(self, obj):
        return obj.zona.nombre

    def get_proyecto(selfself,obj):
        queryset = obj.proyectoconservacion_set.all().filter()
        result = dict()
        if(len(queryset)>0):
            result['codigo'] = queryset[0].codigo
            result['nombre'] = queryset[0].nombre
        return result



class PuntoGeograficoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PuntoGeografico
        fields = ['id','nombre']