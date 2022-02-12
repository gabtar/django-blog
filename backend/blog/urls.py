from django.urls import path, include

from rest_framework.routers import SimpleRouter

from blog.views import CommentViewSet, PostViewSet, UserCreate, UserViewSet, CustomObtainAuthToken

app_name = 'blog'

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='update')

urlpatterns = [
    path('', include(router.urls)),
    path('users/create/', UserCreate.as_view(), name='user-create'),
    path('users/auth/', CustomObtainAuthToken.as_view(), name='user-auth'),
]
