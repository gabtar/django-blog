from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de Post """
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)


class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo de usuario """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'is_author')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Actualiza parámetros del usuario """
        password = validated_data.get('password', None)
        is_author = validated_data.get('is_author', False)

        instance.is_author = bool(is_author)

        if password:
            try:
                validate_password(password)
                instance.set_password(password)
            except:
                raise serializers.ValidationError('Password inseguro')

        instance.save()

        return instance


