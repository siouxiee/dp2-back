# social_management/serializers.py
from rest_framework import serializers
from .models import CuentaRedSocial
from .models import Post

class CuentaRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaRedSocial
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')