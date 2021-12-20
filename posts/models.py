from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import models


class UserManager(BaseUserManager):
    """" Control para la creacion de usuarios del blog"""

    def create_user(self, email, password):
        try:
            validate_password(password)
        except:
            raise ValueError("Password insegura.")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
       """" Modelo de usuario del blog """ 
       email = models.EmailField(max_length=255, unique=True)
       
       is_active = models.BooleanField(default=True)
       is_staff = models.BooleanField(default=False)

       objects = UserManager()

       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = ()

       def __str__(self):
           return self.email


class Post(models.Model):
    """ Modelo para post del blog """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
