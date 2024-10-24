from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
# Create your views here.
from .models import Question,Response, Encuesta, Answer
from .serializers import QuestionSerializer,ResponseSerializer, EncuestaSerializer, AnswerSerializer

@api_view(['GET'])
def obtener_encuestas(request):
    # Obtener los parámetros de la solicitud
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', 10))
    estado = request.query_params.get('estado')

    # Filtrar encuestas por estado si se proporciona
    encuestas = Encuesta.objects.all()
    if estado:
        encuestas = encuestas.filter(status=estado)

    # Obtener la cantidad total de encuestas filtradas
    total_encuestas = encuestas.count()

    # Aplicar la paginación con offset y limit
    encuestas = encuestas[offset:offset + limit]

    # Serializar los datos (excluir preguntas y respuestas)
    encuestas_data = [
        {
            "id": encuesta.id,
            "title": encuesta.title,
            "description": encuesta.description,
            "status": encuesta.status,
            "start_date": encuesta.start_date,
            "end_date": encuesta.end_date
        }
        for encuesta in encuestas
    ]

    # Preparar la respuesta con metadatos y datos de encuestas
    response_data = {
        "metadata": {
            "result_set": {
                "count": len(encuestas_data),
                "offset": offset,
                "limit": limit,
                "total": total_encuestas
            }
        },
        "data": encuestas_data
    }

    # Retornar la respuesta
    return Response(response_data)

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
