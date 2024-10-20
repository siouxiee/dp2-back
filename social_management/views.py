from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CuentaRedSocial
from .models import Post
from .serializers import CuentaRedSocialSerializer
from .serializers import PostSerializer

# Vista para crear y guardar una nueva cuenta de red social
@api_view(['POST'])
def crear_cuenta_red_social(request):
    serializer = CuentaRedSocialSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para consultar las credenciales de una cuenta de red social
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
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)