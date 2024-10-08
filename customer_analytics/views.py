from django.shortcuts import render
from django.http import JsonResponse
from .models import Ciudad, Usuario, Producto, ProductoXUsuario, TipoProducto, Subcategoria

# Servicio para obtener la audiencia por ciudad
def obtenerAudienciaPorCiudad(request):
    ciudades = Ciudad.objects.all()
    data = []
    for ciudad in ciudades:
        usuarios_ciudad = Usuario.objects.filter(direccion__distrito=ciudad.nombre).count()
        data.append({
            'ciudad': ciudad.nombre,
            'audiencia': usuarios_ciudad
        })
    
    return JsonResponse({'audiencia': data})

# Servicio para obtener ventas por sabor
def obtenerVentasPorSabor(request):
    # Asumiendo que "sabores" están categorizados por Subcategoria
    subcategorias = Subcategoria.objects.all()
    ventas = {}
    
    for subcategoria in subcategorias:
        productos = Producto.objects.filter(subcategoria=subcategoria)
        cantidad = ProductoXUsuario.objects.filter(producto__in=productos).count()
        ventas[subcategoria.nombre] = cantidad
    
    return JsonResponse({'ventas_sabores': ventas})

def obtenerVentasPorProducto(request):
    tipos_producto = TipoProducto.objects.all()
    ventas = {}
    
    for tipo in tipos_producto:
        productos_tipo = Producto.objects.filter(tipo_producto=tipo)
        cantidad = ProductoXUsuario.objects.filter(producto__in=productos_tipo).count()
        ventas[tipo.nombre] = cantidad
    
    return JsonResponse({'ventas_tamanos': ventas})
