from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from blog.permissions import IsBlogAuthor, IsUserOwner, PostPermissions
from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer


class UserCreate(generics.CreateAPIView):
    """ Endpoint para creación de usuarios """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserUpdatePassword(generics.UpdateAPIView):
    """ Endpoint para actualizar el password del usuario """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,IsUserOwner,)

    def get_object(self):
        return self.request.user


class UserUpdateIsAuthor(generics.UpdateAPIView):
    """ Endpoint para establecer a un usuario como autor del blog """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,IsBlogAuthor,)


class PostViewSet(viewsets.ModelViewSet):
    """ Viewset para manejar los endpoint del modelo de post """
    permission_classes = (PostPermissions,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


