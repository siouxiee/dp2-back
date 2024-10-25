from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets,status
from rest_framework.response import Response
# Create your views here.
from .models import Question,Response as ResponseModel, Encuesta, Answer
from .serializers import QuestionSerializer,ResponseSerializer, EncuestaSerializer, AnswerSerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST','GET'])
def crear_encuesta(request):
    # Usar el serializer para validar y crear la encuesta
    serializer = EncuestaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(['GET'])
def obtener_encuesta_por_id(request, survey_id):
    try:
        # Buscar la encuesta por su ID
        encuesta = Encuesta.objects.get(id=survey_id)
    except Encuesta.DoesNotExist:
        # Si no se encuentra la encuesta, devolver un error 404
        return Response({"detail": "Encuesta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
    
    # Serializar la encuesta, incluyendo preguntas y respuestas relacionadas
    encuesta_data = {
        "id": encuesta.id,
        "title": encuesta.title,
        "description": encuesta.description,
        "status": encuesta.status,
        "start_date": encuesta.start_date,
        "end_date": encuesta.end_date,
        "questions": [
            {
                "id": question.id,
                "title": question.title,
                "type": question.type,
                "options": question.options or [],
            }
            for question in encuesta.questions.all()
        ],
        "responses": [
            {
                "id": response.id,
                "date": response.date,
                "answers": [
                    {
                        "question_id": answer.question_id,
                        "answer": answer.answer,
                    }
                    for answer in response.answers.all()
                ]
            }
            for response in encuesta.responses.all()
        ]
    }

    # Devolver la respuesta con los datos de la encuesta
    return Response(encuesta_data, status=status.HTTP_200_OK)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer

class EncuestaViewSet(viewsets.ModelViewSet):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
