from rest_framework import permissions


class UpdateAcceptedProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id.id == request.user.id


class UpdateAcceptedMilestone(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id.id == request.user.id
