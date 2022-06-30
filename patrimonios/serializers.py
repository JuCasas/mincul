from rest_framework import serializers

from authentication.models import User
from mincul_app.models import Documento
from patrimonios.models import Institucion, Patrimonio, Categoria, Propietario, Responsable


class InstitucionSerializer(serializers.ModelSerializer):
    dir = serializers.SerializerMethodField('getDir')

    def getDir(self,obj):
        dir = Institucion.objects.get(pk=obj.pk)
        if dir != None:
            if dir.direccion != None:
                return dir.direccion
        return '-'

    class Meta:
        model = Institucion
        fields = ['pk','id','nombre','dir']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','id','first_name','last_name']

class PatrimonioListSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField('getImg')
    categoria = serializers.SerializerMethodField('getCategory')
    tipo = serializers.SerializerMethodField('getTipo')

    def getImg(self, obj):
        doc = Documento.objects.filter(patrimonio__id=obj.pk).first()
        if doc != None:
            return '/'+str(doc.url)
        return '/static/img/imageNotAvailable.jpg'

    def getCategory(self,obj):
        cat = Categoria.objects.get(pk=obj.categoria_id).nombre
        return cat

    def getTipo(self,obj):
        tipo = Patrimonio._meta.get_field('tipoPatrimonio').choices[int(obj.tipoPatrimonio)-1]
        return tipo

    class Meta:
        model = Patrimonio
        fields = ['pk','id','nombreTituloDemoninacion','tipo','categoria','imagen']

class PatrimonioSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField('getImg')
    categoria = serializers.SerializerMethodField('getCategory')
    tipo = serializers.SerializerMethodField('getTipo')
    propietario = serializers.SerializerMethodField('getProp')
    responsable = serializers.SerializerMethodField('getResp')

    def getImg(self, obj):
        doc = Documento.objects.filter(patrimonio__id=obj.pk).first()
        if doc != None:
            return '/'+str(doc.url)
        return '/static/img/imageNotAvailable.jpg'

    def getCategory(self, obj):
        cat = Categoria.objects.get(pk=obj.categoria_id).nombre
        return cat

    def getTipo(self, obj):
        tipo = Patrimonio._meta.get_field('tipoPatrimonio').choices[int(obj.tipoPatrimonio) - 1]
        return tipo

    def getProp(self, obj):
        prop = Propietario.objects.filter(patrimonio__id=obj.pk).first()
        if prop != None:
            return prop
        return {'nombre': '-'}

    def getResp(self, obj):
        resp = Responsable.objects.filter(patrimonio__id=obj.pk).first()
        if resp != None:
            return resp
        return {'nombre': '-'}

    class Meta:
        model = Patrimonio
        fields = ['pk','id','nombreTituloDemoninacion','descripcion','observacion','direccion','departamento','provincia','distrito','tipo','categoria','propietario','responsable','imagen']

#class PatrimonioInmaterialSerializer(serializers.ModelSerializer):