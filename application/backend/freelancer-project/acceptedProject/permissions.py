from rest_framework import permissions


class UpdateAcceptedProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if(obj.user_id.id == request.user.id or obj.freelancer_id.id == request.user.id):
            return True
        else:
            return False



class UpdateAcceptedMilestone(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id.id == request.user.id
