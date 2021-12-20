from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from posts.permissions import IsAuthorOrReadOnly
from posts.models import Post
from posts.serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ Viewset para manejar los endpoint del modelo de post """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ Viewset para manejar los endpoint del modelo de usuario """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    """ Endpoint para creación de usuarios """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
