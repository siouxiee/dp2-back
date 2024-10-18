from django.shortcuts import render
# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Post
from .serializer import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
