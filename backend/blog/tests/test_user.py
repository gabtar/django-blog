from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .helpers import create_user

# Endpoints urls
URL_CREATE_USER = reverse('blog:user-create')
URL_AUTH = reverse('blog:user-auth')

URL_USER_CHANGE_PASSWORD = lambda pk : reverse('blog:update-change-password', kwargs={'pk' : pk })
URL_SET_AS_AUTHOR = lambda pk : reverse('blog:update-set-as-author', kwargs={'pk' : pk })

class PublicUserAPITest(TestCase):
    """ Test relacionados con el acceso a la api de creación de usuarios """

    def setUp(self):
        self.client = APIClient()

    def test_user_create_succesful(self):
        """ Comprueba que se pueda crear un usuario desde la API """
        payload = {
                'email': 'test@test.com',
                'password': 'test123456'
        }

        response = self.client.post(URL_CREATE_USER, payload)
        user = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertNotIn('password', response.data)
        self.assertTrue(user)

    def test_cannot_create_user_if_password_is_not_valid(self):
        """ Comprueba que no se pueda crear un usuario si la contrasenia no cumple los requisitos """
        payload = {
                'email': 'test@test.com',
                'password': 'test156'
        }

        response = self.client.post(URL_CREATE_USER, payload)
        user = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(user)
    
    def test_user_can_obtain_auth_token(self):
         """ 
         Comprueba que se pueda obtener el token de autenticación del usuario 
         Nota: La vista por defecto de rest_framework obtain_auth_token requiere
             un post con username y password. 
             Al usar un modelo personalizado para usuarios, se especificó que el 
             username sea el email, por eso la petición debe hacerse con el campo
             username que usa por defecto el modelo de usuario.
         """
         payload = {
                 'username': 'test@test.com',
                 'password': 'test123456'
         }

         user = create_user(email=payload['username'], password=payload['password'])

         response = self.client.post(URL_AUTH, payload)

         self.assertEqual(status.HTTP_200_OK, response.status_code)
         self.assertIn('token', response.data)
         self.assertEquals(user.id, response.data['id'])

    def test_user_cannot_obtain_token_when_invalid_credentials(self):
         """ Comprueba que nose pueda obtener el token si se pasan valores incorrectos """
 
         payload = {
             'username': 'test@test.com',
             'password': 'test123456'
         }
 
         response = self.client.post(URL_AUTH, payload)
 
         self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
         self.assertNotIn('token', response.data)
 
    def test_cant_change_password_if_user_is_not_authenticated(self):
        """ Comprueba que no se pueda cambiar el password de un usuario """
        user = create_user('test@mail.com', '1psw453o')
        payload = {
            'old_password' : '1psw453o',
            'new_password' : 'ouoquwjl;j12345'
        }

        response = self.client.post(URL_USER_CHANGE_PASSWORD(user.id), payload)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
 

class PrivateUserAPITest(TestCase):
    """ Tests relacionados con la modificación del perfil de usuario a través de la api """

    def setUp(self):
        self.author = create_user(
            email='author@test.com',
            password='author123456'
        )
        self.author.is_author = True
        self.author.save()

        self.user = create_user(
            email='test@test.com',
            password='test123456'
        )

        self.client = APIClient()

    def test_user_change_password_new(self):
        """ Comprueba que el usuario pueda cambiar su propio password """
        self.client.force_authenticate(self.user)

        payload = {
            'old_password' : 'test123456',
            'new_password' : 'o8989812345'
        }

        response = self.client.post(URL_USER_CHANGE_PASSWORD(self.user.id), payload)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['new_password']))
    
    def test_cannot_change_password_if_new_password_is_invalid(self):
        """ Comprueba que no se pueda cambiar el password si el nuevo password es invalido """
        self.client.force_authenticate(self.user)

        payload = {
            'old_password' : 'test123456',
            'new_password' : '1234'
        }

        response = self.client.post(URL_USER_CHANGE_PASSWORD(self.user.id), payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['old_password']))

    def test_cannot_change_password_if_old_password_is_invalid(self):
        """ Comprueba que no se pueda cambiar la contrasenia si la contrasenia antigua no es valida """
        self.client.force_authenticate(self.user)

        payload = {
            'old_password' : 'aaaaa',
            'new_password' : 'oupiuoas123878'
        }

        response = self.client.post(URL_USER_CHANGE_PASSWORD(self.user.id), payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('test123456'))

    def test_set_user_as_post_author(self):
        """
        Comprueba que se pueda dar permisos de autor a un usuario
        Sólo los usuarios que ya sean autores del blog pueden otorgar 
        este permiso
        """
        self.client.force_authenticate(self.author)

        payload = {
            'is_author' : 'True',
        }

        response = self.client.post(URL_SET_AS_AUTHOR(self.user.id), payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_author)

    def test_cannot_set_user_as_post_author(self):
        """
        Comprueba que un usuario común no pueda dar permisos de autor
        """
        self.client.force_authenticate(self.user)

        payload = {
            'is_author' : 'True',
        }

        response = self.client.post(URL_SET_AS_AUTHOR(self.user.id), payload)
        self.user.refresh_from_db()

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertFalse(self.user.is_author)

