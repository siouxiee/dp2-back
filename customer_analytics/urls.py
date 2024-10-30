from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    PersonaViewSet, RolViewSet, CiudadViewSet, UbicacionViewSet, 
    DireccionViewSet, UsuarioViewSet, PermisoViewSet, NotificacionViewSet, 
    TipoProductoViewSet, SubcategoriaViewSet, FrutaViewSet, IgvViewSet, 
    ProductoViewSet, PedidoViewSet, VentaViewSet, DetallePedidoViewSet, 
    ProductoFrutaViewSet, TipoProductoSubcategoriaViewSet, 
    ProductoSubcategoriaViewSet
)
from .views import ventas_por_producto, ventas_totales_fecha,ventas_por_producto_por_ciudad,clientes_con_pedido_entregado,frecuencia_compras_por_dia_semana
router = DefaultRouter()
router.register(r'personas', PersonaViewSet)
router.register(r'roles', RolViewSet)
router.register(r'ciudades', CiudadViewSet)
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'direcciones', DireccionViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'permisos', PermisoViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'tipo-productos', TipoProductoViewSet)
router.register(r'subcategorias', SubcategoriaViewSet)
router.register(r'frutas', FrutaViewSet)
router.register(r'igvs', IgvViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'producto-frutas', ProductoFrutaViewSet)
router.register(r'tipo-producto-subcategorias', TipoProductoSubcategoriaViewSet)
router.register(r'producto-subcategorias', ProductoSubcategoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ventas-por-producto/', ventas_por_producto, name='ventas-por-producto'),
    path('ventas-por-producto/<str:id_producto>/', ventas_por_producto, name='ventas-por-producto-detalle'),
    path('cantidades-totales/', ventas_totales_fecha, name='ventas_totales_fecha'),
    path('ventas-por-producto-ciudad/', ventas_por_producto_por_ciudad, name='ventas_por_producto_por_ciudad'),
    path('ventas-por-producto-ciudad/<str:id_ciudad>/', ventas_por_producto_por_ciudad, name='ventas_por_producto_por_ciudad_detalle'),
    path('clientes-con-pedido-entregado/', clientes_con_pedido_entregado, name='clientes_con_pedido_entregado'),
    path('frecuencia-compras-dia-semana/', frecuencia_compras_por_dia_semana, name='frecuencia_compras_dia_semana'),
    path('cantidades-frecuentes-compra/',views.cantidades_frecuentes_compra, name='cantidades_frecuentes_compra'),
]