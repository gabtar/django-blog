from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Comment, Post


class PublicCommentAPITests(TestCase):
    """ Tests relacionados con la api publica de los comentarios del blog """

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.com', password='test12345')
        self.author = get_user_model().objects.create_user(email='author@test.com', password='author12345', is_author=True)
        self.post = Post.objects.create(
            author=self.author,
            title='Test post',
            body='Cuerpo de prueba'
        ) 
        self.post.save()

        self.client = APIClient()
        # TODO Plantear con un generic ViewSet y mixins, ya que listar todos
        # los comentarios no tiene sentido 
        self.URL_COMMENTS = reverse('blog:comments-list')

    def test_can_retrieve_all_comments(self):
        """ Comprueba que se puedan obtener todos los comentarios de un post """

        response = self.client(self.URL_COMMENTS)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

