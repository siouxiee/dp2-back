# social_management/urls.py
from django.urls import path,include
from . import views
from .views import crear_post
from .views import UploadVideoToS3View, publicar_video
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, vincular_cuenta, desvincular_cuenta, verificar_renovar_token_api

router = DefaultRouter()
router.register(r'posts', PostViewSet)  # La ruta base será /posts/

urlpatterns = [
    path('cuentas/vincular/', vincular_cuenta, name='vincular_cuenta'),
    path('cuentas/desvincular/', desvincular_cuenta, name='desvincular_cuenta'),    
    path('cuentas/verificar-renovar/', verificar_renovar_token_api, name='verificar_renovar_token_api'), #solo es una prueba


    path('cuentas/', views.obtener_cuentas_red_social, name='obtener_cuentas_red_social'),
    path('posts/programados/', views.obtener_posts_programados, name='obtener_posts_programados'),
    path('posts/crear/', crear_post, name='crear_post'),
    path('videos/upload/', UploadVideoToS3View.as_view(), name='upload_video_to_s3'),
    path('videos/publicar/', publicar_video, name='publicar_video_tiktok'),
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
]
