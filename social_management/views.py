from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import CuentaRedSocial, Post, RedSocial
from .serializers import CuentaRedSocialSerializer, PostSerializer, RedSocialSerializer
from .services import publicar_video_tiktok
import boto3
from botocore.exceptions import NoCredentialsError
from smmproject import settings
from django.db.models import Q
from django.http import Http404 

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UploadVideoToS3View(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('video')

        if not video_file:
            return Response({"error": "No se ha proporcionado un archivo de video"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Inicializamos el cliente de S3 con las credenciales proporcionadas
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        try:
            # Subir archivo a S3
            s3.upload_fileobj(video_file, settings.AWS_STORAGE_BUCKET_NAME, video_file.name, ExtraArgs={'ContentType': video_file.content_type})
            
            # Generar la URL del archivo subido
            url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{video_file.name}"
            
            return Response({"message": "Archivo subido con éxito", "url": url}, status=status.HTTP_200_OK)

        except NoCredentialsError:
            return Response({"error": "Credenciales de AWS no encontradas"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def crear_red_social(request):
    serializer = RedSocialSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listar_redes_sociales(request):
    redes = RedSocial.objects.all()
    serializer = RedSocialSerializer(redes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def crear_cuenta_red_social(request):
    serializer = CuentaRedSocialSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_cuentas_red_social(request):
    cuentas = CuentaRedSocial.objects.all()
    serializer = CuentaRedSocialSerializer(cuentas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def eliminar_token(request, pk):
    try:
        cuenta = CuentaRedSocial.objects.get(pk=pk)
    except CuentaRedSocial.DoesNotExist:
        return Response({"error": "Cuenta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    cuenta.delete()
    return Response({"message": "Token eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def obtener_posts_programados(request):
    # Filtra los posts programados
    posts_programados = Post.objects.filter(estado='P')
    # Serializa los datos
    serializer = PostSerializer(posts_programados, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_post(request):
    usuario = request.data.get('usuario')
    try:
        cuenta = CuentaRedSocial.objects.get(usuario=usuario)

        # Verificar si el token expira en menos de 1 día y renovarlo
        if cuenta.fecha_expiracion_token <= datetime.now() + timedelta(days=1):
            if not renovar_token_largo_duracion(cuenta):
                return Response(
                    {'error': 'No se pudo renovar el token. Intenta vincular la cuenta de nuevo.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Crear el post si el token es válido
        post = Post.objects.create(**request.data)
        return Response({'message': 'Post creado exitosamente.'}, status=status.HTTP_201_CREATED)

    except CuentaRedSocial.DoesNotExist:
        return Response({'error': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def publicar_video(request):
    access_token = request.data.get('access_token')
    nombre_archivo_s3 = request.data.get('nombre_archivo_s3')

    if not access_token or not nombre_archivo_s3:
        return Response({"error": "access_token y nombre_archivo_s3 son requeridos"}, status=400)

    resultado = publicar_video_tiktok(access_token, nombre_archivo_s3)

    if resultado:
        return Response({"message": "Video publicado con éxito", "data": resultado}, status=200)
    else:
        return Response({"error": "Error al publicar el video"}, status=500)
