from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken, Token

from blog.permissions import IsBlogAuthor, IsUserOwner, PostPermissions, UserOwner
from blog.models import Post, Comment
from blog.serializers import PostSerializer, PostListSerializer, UserSerializer, CommentSerializer, PasswordSerializer


class UserCreate(generics.CreateAPIView):
    """ Endpoint para creación de usuarios """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.GenericViewSet):
    """ Viewset para manejar los endpoint del modelo de usuario """
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[UserOwner,])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response('Contrasenia incorrecta', status=status.HTTP_400_BAD_REQUEST)
            password = serializer.validated_data.get('new_password')
            user.set_password(password)
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsBlogAuthor,])
    def set_as_author(self, request, pk=None):
        user = self.get_object()
        user.is_author = True
        user.save()
        return Response("Se han otorgado permisios de autor", status=status.HTTP_200_OK)


class CustomObtainAuthToken(ObtainAuthToken):
    """ Vista para authenticar el usuario y devolver datos """
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class PostViewSet(viewsets.ModelViewSet):
    """ Viewset para manejar los endpoint del modelo de post """
    permission_classes = (PostPermissions,)
    authentication_classes = (TokenAuthentication,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return self.serializer_class
      

class CommentViewSet(viewsets.GenericViewSet,
        mixins.RetrieveModelMixin, 
        mixins.CreateModelMixin, 
        mixins.UpdateModelMixin):
    """ Viewset para manejar los endpoint del modelo de comentario """
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,IsUserOwner)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CommentSerializer
    
    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all().filter(related_post=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data) 
