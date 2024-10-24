from rest_framework import serializers
from .models import CuentaRedSocial
from .models import Post
from .models import RedSocial

class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedSocial
        fields = '__all__'

class CuentaRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaRedSocial
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):

    media = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')