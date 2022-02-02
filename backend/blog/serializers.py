from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from blog.models import Comment, Post

class PostSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de Post """
    created_at = serializers.DateTimeField(format='%a %d, %Y')
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)

class PostListSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de posts para listar en la pagina principal del blog"""
    created_at = serializers.DateTimeField(format='%a %d, %Y')
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Se limita a 200 caracteres
        data["body"] = instance.body_preview()
        return data

class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de usuario """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # En los serializadores se puede usar el metodo "validate_campo" por cada campo(field) a validar
    def validate_password(self, value):
        try:
             validate_password(value)
        except:
            raise serializers.ValidationError("Password insegura")
        return value

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
        

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)

    def validate_new_password(self, value):
        try:
             validate_password(value)
        except:
            raise serializers.ValidationError("Password insegura")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de Comment """
    created_at = serializers.DateTimeField(format='%a %d, %Y', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'related_post', 'user', 'answer_to', 'comment', 'created_at',)
