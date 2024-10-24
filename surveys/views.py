from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
# Create your views here.
from .models import Question,Response, Encuesta, Answer
from .serializers import QuestionSerializer,ResponseSerializer, EncuestaSerializer, AnswerSerializer

@api_view(['GET'])
def obtener_encuestas(request):
    # Obtener los parámetros de filtro de la solicitud
    estado = request.query_params.get('estado')
    limite = request.query_params.get('limite')

    # Filtrar las encuestas según el estado si se proporciona
    encuestas = Encuesta.objects.all()
    if estado:
        encuestas = encuestas.filter(status=estado)

    # Aplicar el límite si se proporciona
    if limite:
        try:
            limite = int(limite)
            encuestas = encuestas[:limite]
        except ValueError:
            return Response({"message": "El parámetro 'limite' debe ser un número entero."}, status=400)

    # Serializar las encuestas sin incluir preguntas ni respuestas
    encuestas_data = [
        {
            "id": encuesta.id,
            "title": encuesta.title,
            "description": encuesta.description,
            "status": encuesta.status,
            "start_date": encuesta.start_date,
            "end_date": encuesta.end_date,
        }
        for encuesta in encuestas
    ]

    # Devolver la respuesta con los datos de las encuestas
    return Response(encuestas_data)

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
