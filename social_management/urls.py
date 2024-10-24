# social_management/urls.py
from django.urls import path, include
from . import views
from .views import UploadVideoToS3View, publicar_video
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, obtener_post_por_id, crear_post, actualizar_post

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [

    path('redes/crear/', views.crear_red_social, name='crear_red_social'),
    path('redes/', views.listar_redes_sociales, name='listar_redes_sociales'),


    path('cuentas/', views.obtener_cuentas_red_social, name='obtener_cuentas_red_social'),
    path('cuentas/crear/', views.crear_cuenta_red_social, name='crear_cuenta_red_social'),
    path('cuentas/eliminar/<int:pk>/', views.eliminar_token, name='eliminar_token'),
    

    path('posts/crear/', crear_post, name='crear_post'),
    path('posts/', views.obtener_posts, name='obtener_posts'),
    path('posts/<str:postId>/', obtener_post_por_id, name='obtener_post_por_id'),
    path('posts/actualizar/<str:postId>/', actualizar_post, name='actualizar_post'),
    path('posts/programados/', views.obtener_posts_programados, name='obtener_posts_programados'),


    path('videos/upload/', UploadVideoToS3View.as_view(), name='upload_video_to_s3'),
    path('videos/publicar/', publicar_video, name='publicar_video_tiktok'),
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
]