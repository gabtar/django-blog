from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Comment, Post


def create_user(email, password):
    return get_user_model().objects.create_user(email, password)


class UserModelTest(TestCase):
    """ Test relacionados con el modelo del usuario """

    def test_user_create_succesful(self):
        """ Comprueba que se pueda crear un modelo de usuario """
        user = create_user(email='test@test.com', password='test12345')

        self.assertTrue(get_user_model().objects.filter(email='test@test.com').exists())


class PostModelTest(TestCase):
    """ Test relacionados con el modelo del post """

    def setUp(self):
        self.user = create_user(email='test@test.com', password='test12345')
        self.post = Post.objects.create(
                author=self.user,
                title='Test title',
                body='Test body',
        )

    def test_post_created_succesful(self):
        """ Comprueba que se pueda crear correctamente un modelo de post """
        author = f'{self.post.author}'
        title = f'{self.post.title}'
        body = f'{self.post.body}'
        self.assertEqual(author, 'test@test.com')
        self.assertEqual(title, 'Test title')
        self.assertEqual(body, 'Test body')


class CommentModelTest(TestCase):
    """ Test relacionados con el modelo de comentarios """

    def setUp(self):
        self.user = create_user(email='test@test.com', password='test12345')
        self.post = Post.objects.create(
                author=self.user,
                title='Test title',
                body='Test body',
        )
        self.post.save()

        self.comment = Comment(
            related_post=self.post,
            user=self.user,
            comment='Comentario de prueba'
        )
        self.comment.save()

    def test_comment_created_succesfull(self):
        """ Comprueba que se pueda crear existosamente un modelo de comentario """
        self.assertEqual('Comentario de prueba',self.comment.comment)
        self.assertEqual(self.user,self.comment.user)

    def test_comment_can_have_many_answers(self):
        """ Comprueba que un comentario pueda tener otros comentarios en respuesta """
        answer_comment_one = Comment(
            related_post=self.post,
            user=self.user,
            comment='Respuesta #1',
            answer_to=self.comment
        )
        answer_comment_one.save()
        answer_comment_two = Comment(
            related_post=self.post,
            user=self.user,
            comment='Respuesta #2',
            answer_to=self.comment
        )
        answer_comment_two.save()

        self.assertEqual(2, len(self.comment.answers.all()))

