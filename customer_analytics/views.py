from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.utils.dateparse import parse_datetime
from django.db.models import Count
from django.db.models.functions import Coalesce
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
def cantidad_ciudades_con_ventas(request):
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    # Validar y parsear las fechas
    if fecha_inicio:
        fecha_inicio = parse_datetime(fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_datetime(fecha_fin)

    if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
        return Response({"message": "Ambas fechas deben estar presentes para el filtro."}, status=400)

    # Filtrar los pedidos entregados dentro del rango de fechas
    pedidos_entregados = Pedido.objects.filter(
        estado__iexact="entregado",
        creado_en__date__range=(fecha_inicio, fecha_fin)
    ).values('id_direccion__id_ciudad').distinct()

    # Contar las ciudades únicas
    cantidad_ciudades = pedidos_entregados.count()

    return Response({"cantidad_ciudades": cantidad_ciudades})

@api_view(['GET'])
def cantidad_pedidos_entregados_por_fecha(request):
    # Obtener los parámetros de fecha
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    # Validar y parsear las fechas
    if fecha_inicio:
        fecha_inicio = parse_datetime(fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_datetime(fecha_fin)
    
    # Validación: ambas fechas deben estar presentes
    if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
        return Response({"message": "Debe proporcionar ambas fechas para el filtro."}, status=400)

    # Filtrar pedidos con estado "entregado" en el rango de fechas y contar
    cantidad_pedidos = Pedido.objects.filter(
        estado__iexact="entregado",
        creado_en__range=(fecha_inicio, fecha_fin)
    ).count() if fecha_inicio and fecha_fin else Pedido.objects.filter(estado__iexact="entregado").count()

    # Devolver solo la cantidad
    return Response({"cantidad_pedidos_entregados": cantidad_pedidos})

@api_view(['GET'])
def cantidades_frecuentes_compra(request):
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    # Validar y parsear las fechas
    if fecha_inicio:
        fecha_inicio = parse_datetime(fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_datetime(fecha_fin)

    if not fecha_inicio or not fecha_fin:
        return Response({"message": "Ambas fechas deben estar presentes y en formato correcto para el filtro."}, status=400)

    # Filtrar los pedidos entregados dentro del rango de fechas
    pedidos_entregados = Pedido.objects.filter(
        estado__iexact="entregado",
        creado_en__range=(fecha_inicio, fecha_fin)
    )
    
    # Anotar cada pedido con el total de productos en sus detalles
    cantidades_por_pedido = pedidos_entregados.annotate(total_productos=Sum('detallepedido__cantidad'))

    # Crear un diccionario para contar las ocurrencias de cada total_productos
    frecuencias = {}
    for pedido in cantidades_por_pedido:
        total_productos = pedido.total_productos
        if total_productos in frecuencias:
            frecuencias[total_productos] += 1
        else:
            frecuencias[total_productos] = 1

    # Convertir a formato de lista para una fácil serialización JSON
    resultado = [{"total_productos": k, "ventas": v} for k, v in frecuencias.items()]

    return Response(resultado)

@api_view(['GET'])
def frecuencia_compras_por_dia_semana(request):
    # Get date filters from query parameters
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    # Validate and parse the dates
    if fecha_inicio:
        fecha_inicio = parse_datetime(fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_datetime(fecha_fin)

    # If one date is provided without the other, return an error
    if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
        return Response({"message": "Both dates must be provided for filtering."}, status=400)

    # Filter "entregado" orders by date range if both dates are present
    pedidos_entregados = Pedido.objects.filter(estado__iexact="entregado")
    if fecha_inicio and fecha_fin:
        pedidos_entregados = pedidos_entregados.filter(creado_en__range=(fecha_inicio, fecha_fin))

    # Retrieve the count of orders grouped by the day of the week
    frecuencia_por_dia = {i: 0 for i in range(7)}  # Initialize with 0 for each day (0=Monday, 6=Sunday)

    # Iterate through the filtered orders and calculate frequency by day of the week
    for pedido in pedidos_entregados:
        day_of_week = pedido.creado_en.weekday()  # Monday=0, Sunday=6
        frecuencia_por_dia[day_of_week] += 1

    # Map day of the week integers to day names
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    resultado = [{"dia": dias_semana[day], "total_pedidos": frecuencia_por_dia[day]} for day in range(7)]

    return Response(resultado)

@api_view(['GET'])
def clientes_con_pedido_entregado(request):
    try:
        # Get date filters from query parameters
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        # Validate and parse the dates
        if fecha_inicio:
            fecha_inicio = parse_datetime(fecha_inicio)
        if fecha_fin:
            fecha_fin = parse_datetime(fecha_fin)

        # If one date is provided without the other, return an error
        if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
            return Response({"message": "Both dates must be provided for filtering."}, status=400)

        # Filter "entregado" orders by date range if both dates are present
        pedidos_entregados = Pedido.objects.filter(estado__iexact="entregado")
        if fecha_inicio and fecha_fin:
            pedidos_entregados = pedidos_entregados.filter(creado_en__range=(fecha_inicio, fecha_fin))
        
        # Get user IDs from filtered orders
        usuarios_con_entrega = pedidos_entregados.values_list('id_usuario', flat=True).distinct()
        print("Usuarios con entrega (IDs):", list(usuarios_con_entrega))
        
        # Retrieve unique Usuario objects based on those IDs
        clientes = Usuario.objects.filter(id__in=usuarios_con_entrega)
        print("Clientes encontrados:", list(clientes.values('id', 'nombre', 'apellido')))
        
        # Convert the queryset to a list of dictionaries
        clientes_list = list(clientes.values('id', 'nombre', 'apellido', 'correo'))
        return Response(clientes_list)
        
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def ventas_por_producto_por_ciudad(request, id_ciudad=None):
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')
    # Validar y parsear las fechas
    if fecha_inicio:
        fecha_inicio = parse_datetime(fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_datetime(fecha_fin)

    if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
        return Response({"message": "Ambas fechas deben estar presentes para el filtro."}, status=400)
    

    if id_ciudad:
        # Filtrar las direcciones que pertenecen a la ciudad especificada
        direcciones_en_ciudad = Direccion.objects.filter(id_ciudad=id_ciudad).values_list('id', flat=True)
        
        # Filtrar los pedidos que tienen direcciones en la ciudad especificada
        pedidos_en_ciudad = Pedido.objects.filter(id_direccion__in=direcciones_en_ciudad, estado__iexact="entregado")
    else:
        pedidos_en_ciudad = Pedido.objects.filter(estado__iexact="entregado")
    
    if fecha_inicio and fecha_fin:
        pedidos_en_ciudad = pedidos_en_ciudad.filter(creado_en__range=(fecha_inicio, fecha_fin))
    
    pedidos_ids=pedidos_en_ciudad.values_list('id', flat=True)
    

    # Filtrar los detalles de pedido que están asociados a los pedidos filtrados
    ventas_por_producto = (
        DetallePedido.objects
        .filter(id_pedido__in=pedidos_ids)
        .values('id_producto')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')
    )

    # Agregar el nombre del producto a cada entrada
    resultados = []
    for venta in ventas_por_producto:
        producto = Producto.objects.get(id=venta['id_producto'])
        resultados.append({
            "producto_id": venta['id_producto'],
            "producto_nombre": producto.nombre,
            "total_vendido": venta['total_vendido']
        })

    return Response(resultados)

@api_view(['GET'])
def ventas_por_producto(request, id_producto=None):
    # Obtener las fechas de inicio y fin de los parámetros de la solicitud
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')
    
    # Validar y parsear las fechas
    if fecha_inicio:
        fecha_inicio = parse_datetime(fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_datetime(fecha_fin)
    
    # Validar si las fechas son válidas
    if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
        return Response({"message": "Ambas fechas deben estar presentes para el filtro."}, status=400)

    # Filtrar pedidos que tienen estado "entregado"
    pedidos_entregados = Pedido.objects.filter(estado__iexact="entregado")

    # Filtrar por rango de fechas si ambos valores están presentes
    if fecha_inicio and fecha_fin:
        pedidos_entregados = pedidos_entregados.filter(creado_en__range=(fecha_inicio, fecha_fin))

    # Obtener los IDs de los pedidos entregados
    pedidos_ids = pedidos_entregados.values_list('id', flat=True)

    # Crear el queryset base de DetallePedido filtrando solo por los pedidos entregados
    queryset = DetallePedido.objects.filter(id_pedido__in=pedidos_ids)

    # Filtrar por id_producto si se proporciona
    if id_producto:
        queryset = queryset.filter(id_producto=id_producto)

    # Agrupar y sumar ventas
    ventas_producto = (
        queryset
        .values('id_producto')
        .annotate(total_ventas=Sum('cantidad'))
        .order_by('-total_ventas')
    )

    # Manejar caso en el que no haya resultados
    if not ventas_producto:
        return Response({"message": "No se encontraron ventas para los criterios especificados."}, status=404)
    
    return Response(ventas_producto)

#final

@api_view(['GET'])
def ventas_totales_fecha(request):
    # Obtener parámetros de fecha de la solicitud
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    # Filtrar las ventas con base en las fechas proporcionadas
    if fecha_inicio and fecha_fin:
        # Parsear las fechas para asegurarse de que sean válidas
        fecha_inicio = parse_datetime(fecha_inicio)
        fecha_fin = parse_datetime(fecha_fin)
        if not fecha_inicio or not fecha_fin:
            return Response({"message": "Formato de fecha no válido. Usar YYYY-MM-DD."}, status=400)

        # Filtrar ventas entre las fechas especificadas
        #ventas = Venta.objects.filter(fecha_venta__range=(fecha_inicio, fecha_fin))
        pedidos_entregados = Pedido.objects.filter(estado__iexact="entregado")
        pedidos_entregados = pedidos_entregados.filter(creado_en__range=(fecha_inicio, fecha_fin))
        #else:
        # Si no se proporcionan fechas, usar todas las ventas
        #ventas = Venta.objects.all()
        #ventas = Pedido.objects.all()

    if fecha_inicio and fecha_fin:
        if not pedidos_entregados.exists():
            return Response({"cantidades_totales": 0})
        else:
            pedidos_ids = pedidos_entregados.values_list('id', flat=True)
            queryset = DetallePedido.objects.filter(id_pedido__in=pedidos_ids)
            cantidad_total = queryset.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    # Devolver la respuesta con el monto total
    return Response({"cantidades_totales": cantidad_total})

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