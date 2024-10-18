from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('fecha_modificacion', 'fecha_creacion')  # Excluir los campos especificados
        #fields = '__all__'