from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from blog.permissions import IsBlogAuthor, IsUserOwner, PostPermissions
from blog.models import Post, Comment
from blog.serializers import PostSerializer, UserSerializer, CommentSerializer


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
    authentication_classes = (TokenAuthentication,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.GenericViewSet,
        mixins.RetrieveModelMixin, 
        mixins.CreateModelMixin, 
        mixins.UpdateModelMixin):
    """ Viewset para manejar los endpoint del modelo de comentario """
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,IsUserOwner)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CommentSerializer

