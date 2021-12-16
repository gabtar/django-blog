from posts.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de Post """
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at')
