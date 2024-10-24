from rest_framework import serializers
from .models import CuentaRedSocial
from .models import Post

class CuentaRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaRedSocial
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    media = serializers.URLField(allow_blank=True, required=False)
    social_media = serializers.CharField(source='red_social.nombre', read_only=True)

    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')