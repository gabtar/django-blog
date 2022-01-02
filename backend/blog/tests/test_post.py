from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Post

from .helpers import create_user, create_post

# Endpoints urls
URL_LIST_ALL_POSTS = reverse('blog:posts-list')  # Action = get
URL_CREATE_POST = reverse('blog:posts-list') # Action = post
URL_LIST_POST = lambda pk : reverse('blog:posts-detail', kwargs={'pk': pk}) # Action = get
URL_MODIFY_POST = lambda pk : reverse('blog:posts-detail', kwargs={'pk' : pk}) # Action = patch


class PublicPostAPITest(TestCase):
    """ Tests relacionados con la api publica para los posts del blog """

    def setUp(self):
        self.user = create_user(email='test@test.com', password='test1234528')
        self.client = APIClient()

        self.post = create_post(
            author=self.user,
            title='Test',
            body='Post de prueba',
        )

    def test_list_all_posts_succesfully(self):
        """ Comprueba que se puedan obtener todos los posts del blog """
        # TODO Configurar el paginador al listar posts
        response = self.client.get(URL_LIST_ALL_POSTS)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.post.title, response.data[0]['title'])
        self.assertEqual(self.post.body, response.data[0]['body'])
        self.assertEqual(len(response.data), 1)

    def test_list_post_deatail_succesfully(self):
        """ Comprueba que se pueda obtener el detalle de un post """
        response = self.client.get(URL_LIST_POST(self.post.id))

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
        response = self.client.post(URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class PrivatePostAPITest(TestCase):
    """ Tests relacionados con la api privada para los posts del blog """

    def setUp(self):
        self.user = create_user(email='test@test.com', password='test1234528')
        self.author = create_user(email='author1@test.com', password='author12345') 
        self.author.is_author = True
        self.author.save()

        self.client = APIClient()

    def test_cannot_create_a_post_if_its_not_author(self):
        """ Comprueba que no se pueda crear un post si no es autor del blog """
        self.client.force_authenticate(self.user)
        payload = {
                'author' : 1,
                'title' : 'Post #2',
                'body' : 'Second post'
        }
        response = self.client.post(URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_can_create_a_post_if_its_an_author(self):
        """ Comprueba que se pueda crear un post """
        self.client.force_authenticate(self.author)
        payload = {
                'author' : 2,
                'title' : 'Post #2',
                'body' : 'Second post'
        }

        response = self.client.post(URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Post.objects.get(pk=1).title, payload['title'])
        self.assertEqual(Post.objects.get(pk=1).body, payload['body'])

    def test_author_can_edit_their_own_post(self):
        """ Comprueba que un autor pueda modificar sus propios post """
        self.client.force_authenticate(self.author)
        post = create_post(
                author=self.author,
                title='Post #2',
                body='Second post'
        )

        payload = {
            'title': 'Titulo editado'
        }

        response = self.client.patch(URL_MODIFY_POST(post.id), payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])

    def test_author_cannot_edit_other_authors_posts(self):
        """ Comprueba que un autor no pueda modificar post de otros autores """
        author_two = create_user(email='author2@test.com', password='sample12345') 
        author_two.is_author = True
        author_two.save()

        post_author_two = create_post(
                author=author_two,
                title='Post #2',
                body='Second post'
        )

        self.client.force_authenticate(self.author) # Se loguea al autor 1
        
        payload = {
            'title': 'Titulo editado'
        }

        response = self.client.patch(URL_MODIFY_POST(post_author_two.id), payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_author_can_delete_their_own_posts(self):
        """ Comprueba que un autor pueda eliminar sus posts """
        self.client.force_authenticate(self.author)
        post = create_post(
                author=self.author,
                title='Post #2',
                body='Second post'
        )

        response = self.client.delete(URL_MODIFY_POST(post.id))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Post.objects.filter(pk=post.id).exists())
        
    def test_author_cannot_delete_other_authors_posts(self):
        """ Comprueba que un autor no pueda eliminar posts de otros autores """
        author_two = create_user(email='author2@test.com', password='sample12345') 
        author_two.is_author = True
        author_two.save()

        post_author_two = create_post(
                author=author_two,
                title='Post #2',
                body='Second post'
        )
        
        self.client.force_authenticate(self.author) # Se loguea al autor 1

        response = self.client.delete(URL_MODIFY_POST(post_author_two.id))

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

