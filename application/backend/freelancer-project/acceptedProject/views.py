from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters


from . import serializers
from . import models
from . import permissions

# Create your views here.


class AcceptedProjectViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.AcceptedProjectSerializer
    queryset = models.AcceptedProject.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateAcceptedProject, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'tags__title', 'category__title', '=user_id__id')

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class AcceptedMilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AcceptedMilestoneSerializer
    queryset = models.AcceptedMilestone.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=acceptedproject_id__id',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateAcceptedMilestone, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)