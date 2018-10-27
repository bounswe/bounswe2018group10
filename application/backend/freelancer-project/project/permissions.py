from rest_framework import permissions

class UpdateProject(permissions.BasePermission):
    '''Defines actions different users can take'''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:   # if user's request doesn't change any data system allows him
                                                         # or her to do whatever want
            return True

        return obj.user_id.id == request.user.id        # system allows user's request if the id of the user who made
                                                        # the request is same with the related id of the changed object