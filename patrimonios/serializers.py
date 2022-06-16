from rest_framework import serializers

from authentication.models import User
from patrimonios.models import Institucion


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id','nombre']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']