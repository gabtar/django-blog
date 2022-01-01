from rest_framework import permissions


class UserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsUserOwner(permissions.BasePermission):
    """
    Solo el propio usuario puede cambiar su password
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsBlogAuthor(permissions.BasePermission):
    """
    Es autor del blog
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_author


class PostPermissions(permissions.BasePermission):
    """
    Permisos para el viewset de los post del blog
    """
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_author if request.user.is_authenticated else False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_author and request.user == obj.author

