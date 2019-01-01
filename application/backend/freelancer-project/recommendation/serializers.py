from rest_framework import serializers

from . import models
from project.models import Project, Tag
from acceptedProject.models import AcceptedProject


class DashboardSerializer(serializers.ModelSerializer):
    '''Defines serializer which converts json request to python objects and vice versa.'''

    class Meta:
        model = Project

        fields = ('id', 'user_id', 'title', 'description', 'tags', 'budget_min', 'budget_max', 'deadline')


class ProjectSerializer(DashboardSerializer):
    pass