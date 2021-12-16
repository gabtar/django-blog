from django.test import TestCase

from django.contrib.auth.models import User
from posts.models import Post


class PostModelTest(TestCase):
    """ Test relacionados con el modelo del post """

    def setUp(self):
        user = User.objects.create_user(username='test', password='123456')
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
        self.assertEqual(author, 'test')
        self.assertEqual(title, 'Test title')
        self.assertEqual(body, 'Test body')
