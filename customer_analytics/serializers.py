from rest_framework import serializers
from .models import Ciudad, Usuario, Producto, TipoProducto, Subcategoria,Persona,Direccion,ProductoFruta,Fruta,Venta,Pedido,Rol,Ubicacion,Permiso,Notificacion,Igv,DetallePedido,TipoProductoSubcategoria,ProductoSubcategoria

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

#class UsuarioSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Usuario
#        fields = '__all__'
class UsuarioSerializer(serializers.ModelSerializer):
    id = serializers.CharField()  # Ensure this is CharField

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo']

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = '__all__'

class FrutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruta
        fields = '__all__'

class IgvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Igv
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class ProductoFrutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoFruta
        fields = '__all__'

class TipoProductoSubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProductoSubcategoria
        fields = '__all__'

class ProductoSubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoSubcategoria
        fields = '__all__'