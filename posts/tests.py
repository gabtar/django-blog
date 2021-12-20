from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post

class UserModelTest(TestCase):
    """ Test relacionados con el modelo del usuario """

    def test_user_create_succesful(self):
        """ Comprueba que se pueda crear un modelo de usuario """
        user = get_user_model().objects.create_user(email='test@test.com', password='test12345')

        self.assertTrue(get_user_model().objects.get(email='test@test.com'))


class PostModelTest(TestCase):
    """ Test relacionados con el modelo del post """

    def setUp(self):
        user = get_user_model().objects.create_user(email='test@test.com', password='test12345')
        user.save()

        post = Post.objects.create(
            author=user,
            title='Test title',
            body='Test body',
        )
        post.save()

    def test_post_created_succesful(self):
        """ Comprueba que se pueda crear correctamente un post """
        post = Post.objects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        body = f'{post.body}'
        self.assertEqual(author, 'test@test.com')
        self.assertEqual(title, 'Test title')
        self.assertEqual(body, 'Test body')

class PublicUserAPITest(TestCase):
    """ Test relacionados con el acceso a la api de creación de usuarios """

    def setUp(self):
        self.client = APIClient()
        self.URL = reverse('posts:create')

    def test_user_create_succesful(self):
        """ Comprueba que se pueda crear un usuario desde la API """
        payload = {
            'email': 'test@test.com',
            'password': 'test123456'
        }

        response = self.client.post(self.URL, payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertNotIn('password', response.data)

    # TODO endpoint para recuperar/resetear password
