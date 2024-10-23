from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .models import (
    Persona, Rol, Ciudad, Ubicacion, Direccion, Usuario, Permiso,
    Notificacion, TipoProducto, Subcategoria, Fruta, Igv, Producto,
    Pedido, Venta, DetallePedido, ProductoFruta, TipoProductoSubcategoria,
    ProductoSubcategoria
)
from .serializers import (
    PersonaSerializer, RolSerializer, CiudadSerializer, UbicacionSerializer, 
    DireccionSerializer, UsuarioSerializer, PermisoSerializer, 
    NotificacionSerializer, TipoProductoSerializer, SubcategoriaSerializer, 
    FrutaSerializer, IgvSerializer, ProductoSerializer, PedidoSerializer, 
    VentaSerializer, DetallePedidoSerializer, ProductoFrutaSerializer, 
    TipoProductoSubcategoriaSerializer, ProductoSubcategoriaSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F

@api_view(['GET'])
def ventas_por_producto(request, id_producto=None):
    if id_producto:
        # Filtrar por el id del producto si se proporciona
        ventas_producto = (
            DetallePedido.objects
            .filter(id_producto=id_producto)
            .values('id_producto')
            .annotate(total_ventas=Sum('subtotal'))
        )
        if not ventas_producto:
            return Response({"message": "No se encontraron ventas para el producto especificado."}, status=404)
    else:
        # Obtener las ventas para todos los productos
        ventas_producto = (
            DetallePedido.objects
            .values('id_producto')
            .annotate(total_ventas=Sum('subtotal'))
            .order_by('-total_ventas')
        )
    
    return Response(ventas_producto)

@api_view(['GET'])
def ventas_totales(request, id_producto=None):
    if id_producto:
        # Filtrar por el id del producto si se proporciona
        ventas_producto = (
            DetallePedido.objects
            .filter(id_producto=id_producto)
            .values('id_producto')
            .annotate(total_ventas=Sum('subtotal'))
        )
        if not ventas_producto:
            return Response({"message": "No se encontraron ventas para el producto especificado."}, status=404)
    else:
        # Obtener las ventas para todos los productos
        ventas_producto = (
            DetallePedido.objects
            .values('id_producto')
            .annotate(total_ventas=Sum('subtotal'))
            .order_by('-total_ventas')
        )
    
    return Response(ventas_producto)


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer

class SubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

class FrutaViewSet(viewsets.ModelViewSet):
    queryset = Fruta.objects.all()
    serializer_class = FrutaSerializer

class IgvViewSet(viewsets.ModelViewSet):
    queryset = Igv.objects.all()
    serializer_class = IgvSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class ProductoFrutaViewSet(viewsets.ModelViewSet):
    queryset = ProductoFruta.objects.all()
    serializer_class = ProductoFrutaSerializer

class TipoProductoSubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = TipoProductoSubcategoria.objects.all()
    serializer_class = TipoProductoSubcategoriaSerializer

class ProductoSubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = ProductoSubcategoria.objects.all()
    serializer_class = ProductoSubcategoriaSerializer