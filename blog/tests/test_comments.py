from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Comment
from .helpers import create_user, create_comment, create_post


# Endpoints urls
URL_GET_COMMENTS = lambda pk : reverse('blog:comments-detail', kwargs={'pk' : pk })

URL_CREATE_POST = reverse('blog:comments-list')
URL_UPDATE_COMMENT = lambda pk : reverse('blog:comments-detail', kwargs={'pk' : pk })


class PublicCommentAPITests(TestCase):
    """ Tests relacionados con la api publica de los comentarios del blog """

    def setUp(self):
        self.user = create_user(email='test@test.com', password='test12345')
        self.author = create_user(email='author@test.com', password='author12345')
        self.author.is_author = True
        self.author.save()
        self.post = create_post(
            author=self.author,
            title='Test post',
            body='Cuerpo de prueba'
        ) 

        self.comment = create_comment(
                related_post=self.post,
                user=self.user,
                comment='Test comment'
        )

        self.client = APIClient()

    def test_can_retrieve_all_comments_from_a_post(self):
        """ Comprueba que se puedan obtener todos los comentarios de un post """

        response = self.client.get(URL_GET_COMMENTS(self.post.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.comment.comment, response.data['comment'])


class PrivateCommentAPITests(TestCase):
    """ Tests relacionados con la api privada de los comentarios del blog """

    def setUp(self):
        self.user = create_user(email='test@test.com', password='test12345')
        self.author = create_user(email='author@test.com', password='author12345')
        self.author.is_author = True
        self.author.save()
        self.post = create_post(
            author=self.author,
            title='Test post',
            body='Cuerpo de prueba'
        ) 

        self.comment = create_comment(
                related_post=self.post,
                user=self.user,
                comment='Test comment'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_can_create_a_comment_in_a_post(self):
        """ Comprueba que se pueda crear un comentario en un determinado post """
        payload = {
            'related_post' : self.post.id,
            'user' : self.user.id,
            'comment' : "Sample comment"
        }

        response = self.client.post(URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Comment.objects.get(pk=response.data['id']).comment, response.data['comment'])

    def test_can_create_an_aswer_to_other_comment(self):
        """ Comprueba que se pueda crear una respuesta a otro comentario """
        payload = {
            'related_post' : self.post.id,
            'user' : self.user.id,
            'answer_to' : self.comment.id,
            'comment' : "Respuesta"
        }

        response = self.client.post(URL_CREATE_POST, payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Comment.objects.all().get(pk=self.comment.id).answers.count())

    def test_can_modify_own_comment(self):
        """ Comprueba que un usuario pueda modificar un comentario """
        payload = {
            'comment' : 'Comentario editado'
        }

        response = self.client.patch(URL_UPDATE_COMMENT(self.comment.id), payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(payload['comment'], Comment.objects.all().get(pk=self.comment.id).comment)

    def test_cannot_modify_comment_if_authenticated_user_is_not_owner(self):
        """ Comprueba que un usuario no pueda modificar un comentario de otro """
        self.client.logout()
        
        self.client.force_authenticate(self.author)

        payload = {
            'comment' : 'Comentario editado'
        }

        response = self.client.patch(URL_UPDATE_COMMENT(self.comment.id), payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
