from rest_framework import serializers

from authentication.models import User
from mincul_app.models import Documento
from patrimonios.models import Institucion, Patrimonio, Categoria


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id','nombre']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class PatrimonioListSerializer(serializers.ModelSerializer):

    imagen = serializers.SerializerMethodField('getImg')
    categoria = serializers.SerializerMethodField('getCategory')
    tipo = serializers.SerializerMethodField('getTipo')

    def getImg(self, obj):
        doc = Documento.objects.filter(patrimonio__id=obj.pk).first()
        if doc != None:
            return str(doc.url)
        return 'static/img/imageNotAvailable.jpg'

    def getCategory(self,obj):
        cat = Categoria.objects.get(pk=obj.categoria_id).nombre
        return cat

    def getTipo(self,obj):
        tipo = Patrimonio._meta.get_field('tipoPatrimonio').choices[int(obj.tipoPatrimonio)-1]
        return tipo

    class Meta:
        model = Patrimonio
        fields = ['id','nombreTituloDemoninacion','tipo','categoria','imagen']

class PatrimonioSerializer(serializers.ModelSerializer):

    imagen = serializers.SerializerMethodField('getImg')
    categoria = serializers.SerializerMethodField('getCategory')
    tipo = serializers.SerializerMethodField('getTipo')

    def getImg(self, obj):
        doc = Documento.objects.filter(patrimonio__id=obj.pk).first()
        if doc != None:
            return '/'+str(doc.url)
        return 'static/img/imageNotAvailable.jpg'

    def getCategory(self, obj):
        cat = Categoria.objects.get(pk=obj.categoria_id).nombre
        return cat

    def getTipo(self, obj):
        tipo = Patrimonio._meta.get_field('tipoPatrimonio').choices[int(obj.tipoPatrimonio) - 1]
        return tipo

    class Meta:
        model = Patrimonio
        fields = ['id','nombreTituloDemoninacion','descripcion','observacion','direccion','departamento','provincia','distrito','tipo','categoria','imagen']