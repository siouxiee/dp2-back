from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    PersonaViewSet, RolViewSet, CiudadViewSet, UbicacionViewSet, 
    DireccionViewSet, UsuarioViewSet, PermisoViewSet, NotificacionViewSet, 
    TipoProductoViewSet, SubcategoriaViewSet, FrutaViewSet, IgvViewSet, 
    ProductoViewSet, PedidoViewSet, VentaViewSet, DetallePedidoViewSet, 
    ProductoFrutaViewSet, TipoProductoSubcategoriaViewSet, 
    ProductoSubcategoriaViewSet,PromocionViewSet
)
from .views import( ventas_por_producto, ventas_totales_fecha,ventas_por_producto_por_ciudad,clientes_con_pedido_entregado,
                   frecuencia_compras_por_dia_semana,ventas_por_promocion,cantidad_pedidos_cancelados,edades_frecuentes_clientes,
                   top_clientes_por_pedidos,ventas_totales_monto)
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
router.register(r'promociones', PromocionViewSet)


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
    path('cantidad-pedidos-entregados-por-fecha/', views.cantidad_pedidos_entregados_por_fecha, name='pedidos_entregados_por_fecha'),
    path('cantidad-ciudades-ventas/', views.cantidad_ciudades_con_ventas, name='cantidad_ciudades_ventas'),
    path('ventas-por-promocion/', views.ventas_por_promocion, name='ventas_por_promocion'),
    path('ventas-por-promocion/<str:id_promocion>/', ventas_por_promocion, name='ventas_por_promocion'),
    path('cantidad-pedidos-cancelados/', cantidad_pedidos_cancelados, name='cantidad_pedidos_cancelados'),
    path('edades-frecuentes-clientes/', edades_frecuentes_clientes, name='edades_frecuentes_clientes'),
    path('top-clientes-por-pedidos/', top_clientes_por_pedidos, name='top_clientes_por_pedidos'),
    path('ventas-totales-monto/', ventas_totales_monto, name='ventas_totales_monto'),
]