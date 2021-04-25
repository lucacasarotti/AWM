from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from utenti.models import Profile


class IsSameAnagraficaUserOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari dei dati loggati.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsSameUserOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari dei dati loggati.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id



class IsRecensionePossessorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_recensore == request.user


class IsUserLogged(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

