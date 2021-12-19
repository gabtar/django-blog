from posts.models import Post
from django.contrib.auth import get_user_model
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de Post """
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)


class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de usuario base de django """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)
