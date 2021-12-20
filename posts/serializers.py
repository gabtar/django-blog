from posts.models import Post
from django.contrib.auth import get_user_model
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de Post """
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)


class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de usuario """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
