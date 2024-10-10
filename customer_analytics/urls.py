from django.urls import path
from . import views

urlpatterns = [
    path('audiencia-ciudad/', views.obtenerAudienciaPorCiudad, name='audienciaCiudad'),
    path('ventas-sabor/', views.obtenerVentasPorSabor, name='ventasSabor'),
    path('ventas-producto/', views.obtenerVentasPorProducto, name='ventasProducto'),
]