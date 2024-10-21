from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Ciudad, Usuario, Producto, ProductoXUsuario, TipoProducto, Subcategoria
from .serializers import CiudadSerializer, UsuarioSerializer, ProductoSerializer, ProductoXUsuarioSerializer, TipoProductoSerializer, SubcategoriaSerializer

# Servicio para obtener la audiencia por ciudad
@api_view(['GET'])
def obtenerAudienciaPorCiudad(request):
    ciudades = Ciudad.objects.all()
    data = []
    for ciudad in ciudades:
        usuarios_ciudad = Usuario.objects.filter(direccion__distrito=ciudad.nombre).count()
        data.append({
            'ciudad': ciudad.nombre,
            'audiencia': usuarios_ciudad
        })
    return Response({'audiencia': data})

# Servicio para obtener ventas por sabor
@api_view(['GET'])
def obtenerVentasPorSabor(request):
    subcategorias = Subcategoria.objects.all()
    ventas = {}
    
    for subcategoria in subcategorias:
        productos = Producto.objects.filter(subcategoria=subcategoria)
        cantidad = ProductoXUsuario.objects.filter(producto__in=productos).count()
        ventas[subcategoria.nombre] = cantidad
    
    return Response({'ventas_sabores': ventas})

# Servicio para obtener ventas por producto
@api_view(['GET'])
def obtenerVentasPorProducto(request):
    tipos_producto = TipoProducto.objects.all()
    ventas = {}
    
    for tipo in tipos_producto:
        productos_tipo = Producto.objects.filter(tipo_producto=tipo)
        cantidad = ProductoXUsuario.objects.filter(producto__in=productos_tipo).count()
        ventas[tipo.nombre] = cantidad
    
    return Response({'ventas_tamanos': ventas})
