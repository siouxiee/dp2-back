from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Ciudad, Usuario, Producto, TipoProducto, Subcategoria
from .serializers import CiudadSerializer, UsuarioSerializer, ProductoSerializer, TipoProductoSerializer, SubcategoriaSerializer


