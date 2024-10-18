# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)  # La ruta base será /posts/

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
]
