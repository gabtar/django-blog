from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Solo el autor puede modificar los posts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsUserOwner(permissions.BasePermission):
    """
    Solo el propio usuario puede cambiar su password
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsBlogAuthor(permissions.BasePermission):
    """
    Es autor del blog
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_author
