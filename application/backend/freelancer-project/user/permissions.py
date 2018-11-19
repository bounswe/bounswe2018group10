from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class UpdateUser(permissions.BasePermission):
    """Allow users to update their own user information such as email, name and password."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateClientProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class UpdateFreelancerProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class ViewProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id
