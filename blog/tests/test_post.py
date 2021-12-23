from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Post


class PublicPostAPITest(TestCase):
    """ Tests relacionados con la api publica para los posts del blog """

    def setUp(self):
        self.user = get_user_model().objects.create(email='test@test.com', password='test1234528')
        self.client = APIClient()

        self.post = Post.objects.create(
            author=self.user,
            title='Test',
            body='Post de prueba',
        )
        self.post.save()

        # Urls del ModelViewSet con SimpleRouter()
        self.URL_LIST_ALL_POSTS = reverse('blog:posts-list')  # Action = get
        self.URL_LIST_POST = reverse('blog:posts-detail', kwargs={'pk': 1}) # Action = get
        self.URL_CREATE_POST = reverse('blog:posts-list') # Action = post

    def test_list_all_posts_succesfully(self):
        """ Comprueba que se puedan obtener todos los posts del blog """
        # TODO Configurar el paginador al listar posts
        response = self.client.get(self.URL_LIST_ALL_POSTS)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.post.title, response.data[0]['title'])
        self.assertEqual(self.post.body, response.data[0]['body'])
        self.assertEqual(len(response.data), 1)


    def test_list_post_deatail_succesfully(self):
        """ Comprueba que se pueda obtener el detalle de un post """
        response = self.client.get(self.URL_LIST_POST)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.post.title, response.data['title'])
        self.assertEqual(self.post.body, response.data['body'])


class PrivatePostAPITest(TestCase):
    """ Tests relacionados con la api privada para los posts del blog """

    def setUp(self):
        self.user = get_user_model().objects.create(email='test@test.com', password='test1234528')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        # Urls del ModelViewSet con SimpleRouter()
        self.URL_LIST_ALL_POSTS = reverse('blog:posts-list')  # Action = get
        self.URL_LIST_POST = reverse('blog:posts-detail', kwargs={'pk': 1}) # Action = get
        self.URL_CREATE_POST = reverse('blog:posts-list') # Action = post

    def test_create_new_post(self):
        """ Comprueba que se pueda crear un post """
        # TODO verificar los permisos
        payload = {
                'author' : 1,
                'title' : 'Post #2',
                'body' : 'Second post'
        }
        response = self.client.post(self.URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
