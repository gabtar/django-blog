from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

from blog.views import PostViewSet, UserCreate, UserUpdatePassword, UserUpdateIsAuthor

app_name = 'blog'

router = SimpleRouter()
router.register(r'', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('users/create/', UserCreate.as_view(), name='user-create'),
    path('users/auth/', obtain_auth_token, name='user-auth'),
    path('users/update_pass/', UserUpdatePassword.as_view(), name='user-update-pass'),
    path('users/set_author/<int:pk>', UserUpdateIsAuthor.as_view(), name='user-set-author'),
]
