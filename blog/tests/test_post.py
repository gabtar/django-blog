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

    def test_cannot_create_post_if_not_authenticated(self):
        """ Comprueba que no se pueda crear un post si el usuario no está autenticado """
        payload = {
                'author' : 1,
                'title' : 'Post #2',
                'body' : 'Second post'
        }
        response = self.client.post(self.URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class PrivatePostAPITest(TestCase):
    """ Tests relacionados con la api privada para los posts del blog """

    def setUp(self):
        self.user = get_user_model().objects.create(email='test@test.com', password='test1234528')
        self.author = get_user_model().objects.create(email='author1@test.com', password='author12345', is_author = True) 
        self.client = APIClient()

        # Urls del ModelViewSet con SimpleRouter()
        self.URL_CREATE_POST = reverse('blog:posts-list') # Action = post
        self.URL_MODIFY_POST = reverse('blog:posts-detail', kwargs={'pk' : 1}) # Action = patch

    def test_cannot_create_a_post_if_its_not_author(self):
        """ Comprueba que no se pueda crear un post si no es autor del blog """
        self.client.force_authenticate(self.user)
        payload = {
                'author' : 1,
                'title' : 'Post #2',
                'body' : 'Second post'
        }
        response = self.client.post(self.URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_can_create_a_post_if_its_an_author(self):
        """ Comprueba que se pueda crear un post """
        self.client.force_authenticate(self.author)
        payload = {
                'author' : 2,
                'title' : 'Post #2',
                'body' : 'Second post'
        }

        response = self.client.post(self.URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Post.objects.get(pk=1).title, payload['title'])
        self.assertEqual(Post.objects.get(pk=1).body, payload['body'])

    def test_author_can_edit_their_own_post(self):
        """ Comprueba que un autor pueda modificar sus propios post """
        self.client.force_authenticate(self.author)
        post = Post.objects.create(
                author=self.author,
                title='Post #2',
                body='Second post'
        )
        post.save()

        payload = {
            'title': 'Titulo editado'
        }

        response = self.client.patch(self.URL_MODIFY_POST, payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])

    def test_author_cannot_edit_other_authors_posts(self):
        """ Comprueba que un autor no pueda modificar post de otros autores """
        author_two = get_user_model().objects.create(email='author2@test.com', password='sample12345', is_author = True) 
        author_two.save()

        post_author_two = Post.objects.create(
                author=author_two,
                title='Post #2',
                body='Second post'
        )
        post_author_two.save()

        self.client.force_authenticate(self.author) # Se loguea al autor 1
        
        payload = {
            'title': 'Titulo editado'
        }

        response = self.client.patch(self.URL_MODIFY_POST, payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_author_can_delete_their_own_posts(self):
        """ Comprueba que un autor pueda eliminar sus posts """
        self.client.force_authenticate(self.author)
        post = Post.objects.create(
                author=self.author,
                title='Post #2',
                body='Second post'
        )
        post.save()

        response = self.client.delete(self.URL_MODIFY_POST)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Post.objects.filter(pk=1).exists())
        
    def test_author_cannot_delete_other_authors_posts(self):
        """ Comprueba que un autor no pueda eliminar posts de otros autores """
        author_two = get_user_model().objects.create(email='author2@test.com', password='sample12345', is_author = True) 
        author_two.save()

        post_author_two = Post.objects.create(
                author=author_two,
                title='Post #2',
                body='Second post'
        )
        post_author_two.save()
        
        self.client.force_authenticate(self.author) # Se loguea al autor 1

        response = self.client.delete(self.URL_MODIFY_POST)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

