from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
# Create your views here.
from .models import Question,Response, Encuesta, Answer
from .serializers import QuestionSerializer,ResponseSerializer, EncuestaSerializer, AnswerSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class EncuestaViewSet(viewsets.ModelViewSet):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    