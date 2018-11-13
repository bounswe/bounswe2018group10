from rest_framework import permissions


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

        return obj.user_id.id == request.user.id

class UpdateFreelancerProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id.id == request.user.id