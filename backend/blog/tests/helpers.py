from django.contrib.auth import get_user_model
from blog.models import Post, Comment
# Funciones auxiliares para crear modelos en los tests

def create_user(email, password):
    return get_user_model().objects.create_user(email, password)

def create_post(author, title, body):
    post = Post.objects.create(author=author, title=title, body=body)
    post.save()
    return post

def create_comment(related_post, user, comment):
    comment = Comment.objects.create(related_post=related_post, user=user, comment=comment)
    comment.save()
    return comment
