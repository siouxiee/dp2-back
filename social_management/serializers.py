from rest_framework import serializers
from .models import CuentaRedSocial, Post

class CuentaRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaRedSocial
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    media = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
