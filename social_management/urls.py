# social_management/urls.py
from django.urls import path
from . import views
from .views import crear_post

urlpatterns = [
    path('cuentas/', views.obtener_cuentas_red_social, name='obtener_cuentas_red_social'),
    path('cuentas/crear/', views.crear_cuenta_red_social, name='crear_cuenta_red_social'),
    path('posts/programados/', views.obtener_posts_programados, name='obtener_posts_programados'),
    path('posts/crear/', crear_post, name='crear_post'),
]
