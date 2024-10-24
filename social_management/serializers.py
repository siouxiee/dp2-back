# social_management/serializers.py
from rest_framework import serializers
from .models import CuentaRedSocial
from .models import Post

class CuentaRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaRedSocial
        fields = '__all__'

class DesvincularCuentaSerializer(serializers.Serializer):
    red_social = serializers.CharField(max_length=50)
    usuario = serializers.CharField(max_length=100)

#class PostSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Post
#        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')  # Excluir los campos especificados
        #fields = '__all__'