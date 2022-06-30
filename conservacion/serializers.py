import os

from rest_framework import serializers
from conservacion.models import ProyectoConservacion, Tarea, Campo
from conservacion.models import Actividad
from mincul_app.models import Documento
from authentication.models import User
from patrimonios.models import Institucion, Patrimonio, Categoria, Propietario, Responsable


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
        fields = ['id','codigo','nombre','descripcion','fechaRegistro','fecha','presupuesto','gasto', 'status']
        #                                               fechaInicio   , fechaFin

class PatrimonioSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField('getImg')
    categoria = serializers.SerializerMethodField('getCategory')
    tipo = serializers.SerializerMethodField('getTipo')

    def getImg(self, obj):
        doc = Documento.objects.filter(patrimonio__id=obj.pk).first()
        if doc != None:
            return str(doc.url)
        return '/static/img/imageNotAvailable.jpg'

    def getCategory(self, obj):
        cat = Categoria.objects.get(pk=obj.categoria_id).nombre
        return cat

    def getTipo(self, obj):
        tipo = Patrimonio._meta.get_field('tipoPatrimonio').choices[int(obj.tipoPatrimonio) - 1]
        return tipo

    class Meta:
        model = Patrimonio
        fields = ['pk', 'id', 'nombreTituloDemoninacion', 'tipo', 'categoria', 'imagen']

class ConservadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'codigo', 'first_name', 'last_name']

class DocumentoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Documento
        fields = ['id','name','url']
    def get_name(self, instance):
        return os.path.basename(instance.url.name)


class RelacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actividad
        fields = ['id','codigo','nombre']

class ActividadSerializer (serializers.ModelSerializer):

    fechaFin = serializers.DateField(format='%d/%m/%Y', required=False)
    patrimonio = serializers.CharField(source='patrimonio.nombreTituloDemoninacion')
    patrimonioPk = serializers.IntegerField(source='patrimonio.pk')
    conservadores = ConservadorSerializer(read_only=True, many=True)
    documentos = DocumentoSerializer(read_only=True, many=True)
    relaciones = RelacionSerializer(read_only=True, many=True)
    total_conservadores = serializers.SerializerMethodField()
    fechaInicio = serializers.DateField(format='%d/%m/%Y', required=False)

    class Meta:
        model = Actividad
        fields = ['documentos','patrimonioPk','id','codigo','nombre','fechaInicio','fechaFin','presupuesto','gastoTotal','estado','descripcion','status', "patrimonio", "total_conservadores","relaciones","conservadores"]

    def get_total_conservadores(self, instance):
        return instance.conservadores.count()


class SecionSerializer (serializers.ModelSerializer):
    documentos = DocumentoSerializer(read_only=True, many=True)

    class Meta:
        model = Campo
        fields = ['documentos','id','nombre','contenido']

