from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from user.models import User, FreelancerProfile, ClientProfile
from project.models import Project, Tag

from . import models
from . import serializers
from django.db.models.query import QuerySet


# Create your views here.


class DashboardViewSet(viewsets.ReadOnlyModelViewSet):
    #serializer_class = serializers.DashboardSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        user = self.request.user
        if user.is_client():
            return self._get_users_for_client(user)

        # is freelancer
        return self._get_projects_for_freelancer(user)

    def _get_users_for_client(self, user: User):
        profile = ClientProfile.objects.get(user=user)
        freelancer_profile = FreelancerProfile.objects.get(user=user)
        self_id = freelancer_profile.id

        if not profile.tags.count():
            # client has no interests
            return (FreelancerProfile.objects.all().exclude(pk=self_id).distinct())

        return (FreelancerProfile.objects
                .filter(tags__in=profile.tags.all()).exclude(pk=self_id)
                .distinct())

    def _get_projects_for_freelancer(self, user: User):
        profile = FreelancerProfile.objects.get(user=user)
        if not profile.tags.count():
            # freelancer has no interests
            return Project.objects.all()

        return (Project.objects
                .filter(tags__in=profile.tags.all())
                .distinct())
    def get_serializer_class(self):
        user = self.request.user
        role = user.role
        if role == user.FREELANCER:
            return serializers.FreelancerDashboardSerializer
        elif role == user.CLIENT:
            return serializers.ClientDashboardSerializer
        else:
            return None


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProjectSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        project_id = int(self.kwargs.get('project_id'))
        project = Project.objects.get(pk=project_id)
        # all related projects except itself
        return (Project.objects
                .filter(tags__in=project.tags.all())
                .exclude(pk=project_id)
                .distinct())
