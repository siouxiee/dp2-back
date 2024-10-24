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
    social_media = serializers.CharField(source='red_social.nombre', read_only=True)

    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')

    def create(self, validated_data):
        social_media_name = self.initial_data.get('social_media')

        try:
            red_social = RedSocial.objects.get(nombre=social_media_name)
        except RedSocial.DoesNotExist:
            raise serializers.ValidationError({'social_media': f'Red social "{social_media_name}" no encontrada.'})

        validated_data['red_social'] = red_social

        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        social_media_name = self.initial_data.get('social_media')

        if social_media_name:
            try:
                red_social = RedSocial.objects.get(nombre=social_media_name)
                validated_data['red_social'] = red_social
            except RedSocial.DoesNotExist:
                raise serializers.ValidationError({'social_media': f'Red social "{social_media_name}" no encontrada.'})

        return super().update(instance, validated_data)