from django.urls import path, include
from rest_framework.routers import SimpleRouter
from posts.views import PostViewSet, UserCreate, UserViewSet

app_name = 'posts'

router = SimpleRouter()
# router.register('users', UserViewSet, basename='users')
router.register('', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('users/create/', UserCreate.as_view(), name='create')
]
