from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """" Control para la creacion de usuarios del blog"""

    def create_user(self, email, password):

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
       """" Modelo de usuario del blog """ 
       email = models.EmailField(max_length=255, unique=True)

       is_active = models.BooleanField(default=True)
       is_author = models.BooleanField(default=False)
       is_staff = models.BooleanField(default=False)

       objects = UserManager()

       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = ()

       def __str__(self):
           return self.email


class Post(models.Model):
    """ Modelo para post del blog """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def body_preview(self):
        """ Devuelve una version acortada del body del post """
        return f'{self.body}'[:100]


class Comment(models.Model):
    """ Modelo para un comentario del blog """
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    answer_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,related_name='answers')
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Post: {self.related_post}, user: {self.user}'
