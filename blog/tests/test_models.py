from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Post


class UserModelTest(TestCase):
    """ Test relacionados con el modelo del usuario """

    def test_user_create_succesful(self):
        """ Comprueba que se pueda crear un modelo de usuario """
        user = get_user_model().objects.create_user(email='test@test.com', password='test12345')

        self.assertTrue(get_user_model().objects.filter(email='test@test.com').exists())


class PostModelTest(TestCase):
    """ Test relacionados con el modelo del post """

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.com', password='test12345')
        self.post = Post.objects.create(
                author=self.user,
                title='Test title',
                body='Test body',
        )

    def test_post_created_succesful(self):
        """ Comprueba que se pueda crear correctamente un post """
        author = f'{self.post.author}'
        title = f'{self.post.title}'
        body = f'{self.post.body}'
        self.assertEqual(author, 'test@test.com')
        self.assertEqual(title, 'Test title')
        self.assertEqual(body, 'Test body')

