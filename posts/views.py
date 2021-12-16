from rest_framework import generics
from posts.models import Post
from posts.serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """ Endpoint para listar y/o crear posts (sólo GET y POST) """
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Endpoint para obtener, actualizar o eliminar un post (GET, PUT, DELETE) """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
