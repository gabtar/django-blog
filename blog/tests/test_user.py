from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class PublicUserAPITest(TestCase):
    """ Test relacionados con el acceso a la api de creación de usuarios """

    def setUp(self):
        self.client = APIClient()
        self.URL_CREATE = reverse('blog:user-create')
        self.URL_AUTH = reverse('blog:user-auth')

    def test_user_create_succesful(self):
        """ Comprueba que se pueda crear un usuario desde la API """
        payload = {
                'email': 'test@test.com',
                'password': 'test123456'
        }

        response = self.client.post(self.URL_CREATE, payload)
        user = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertNotIn('password', response.data)
        self.assertTrue(user)
    
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

         user = get_user_model().objects.create_user(email=payload['username'], password=payload['password'])

         response = self.client.post(self.URL_AUTH, payload)

         self.assertEqual(status.HTTP_200_OK, response.status_code)
         self.assertIn('token', response.data)

    def test_user_cannot_obtain_token_when_invalid_credentials(self):
         """ Comprueba que nose pueda obtener el token si se pasan valores incorrectos """
 
         payload = {
             'username': 'test@test.com',
             'password': 'test123456'
         }
 
         response = self.client.post(self.URL_AUTH, payload)
 
         self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
         self.assertNotIn('token', response.data)
 
     # TODO endpoint para recuperar/resetear password
     # Lo más simple es usar el paquete django-rest-passwordreset
     # Sino habría que probar mandar un token por mail al usuario
     # y que con ese token se pueda acceder a un endpoint para\
     # resetear el password
 
 
class PrivateUserAPITest(TestCase):
    """ Tests relacionados con la modificación del perfil de usuario a través de la api """

    def setUp(self):
        self.author = get_user_model().objects.create_user(
            email='author@test.com',
            password='test123456'
        )
        self.author.is_author = True
        self.author.save()

        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test123456'
        )

        self.client = APIClient()
        self.URL_UPDATE_PASS = reverse('blog:user-update-pass')
        self.URL_SET_AUTHOR = reverse('blog:user-set-author', kwargs={'pk' : self.user.id })

    def test_user_can_change_own_password(self):
        """ 
        Comprueba que el usuario pueda cambiar su password
        """
        self.client.force_authenticate(self.user)

        payload = {
            'password' : 'kjwljpassw12345'
        }

        response = self.client.patch(self.URL_UPDATE_PASS, payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))


    def test_cannot_change_password_if_new_password_is_invalid(self):
        """ 
        Comprueba que no se pueda cambiar la password si el nuevo password no cumple
        los requisitos de seguridad
        """
        self.client.force_authenticate(self.user)

        payload = {
            'password' : '12345'
        }

        response = self.client.patch(self.URL_UPDATE_PASS, payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(self.user.check_password(payload['password']))
    
    def test_cannot_set_user_as_post_author(self):
        """
        Comprueba que un usuario común no pueda dar permisos de autor
        """
        self.client.force_authenticate(self.user)

        payload = {
            'is_author' : 'True',
        }

        response = self.client.patch(self.URL_SET_AUTHOR, payload)
        self.user.refresh_from_db()

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertFalse(self.user.is_author)

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

        response = self.client.patch(self.URL_SET_AUTHOR, payload)
        self.user.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(self.user.is_author)

