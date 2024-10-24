from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet,ResponseViewSet, EncuestaViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'encuestas', EncuestaViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]