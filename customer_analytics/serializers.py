from rest_framework import serializers
from .models import Ciudad, Usuario, Producto, ProductoXUsuario, TipoProducto, Subcategoria

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ['id', 'nombre', 'region']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'precio_a']

class ProductoXUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoXUsuario
        fields = ['id', 'producto', 'usuario', 'esta_activo']

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ['id', 'nombre']

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = ['id', 'nombre']
