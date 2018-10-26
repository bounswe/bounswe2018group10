from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters


from . import serializers
from . import models
from . import permissions

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    '''Handles reading, creating, updating and deleting projects.'''

    serializer_class = serializers.ProjectSerializer    # defines which serializer class will be use for this api
    queryset = models.Project.objects.all()             # tells the viewset how to retrieve data from database
    authentication_classes = (TokenAuthentication,)     # defines which authentication type will be used
    permission_classes = (permissions.UpdateProject, IsAuthenticatedOrReadOnly)   # defines users' permissions
    filter_backends = (filters.SearchFilter,)           # defines which filter type will be used
    search_fields = ('title', 'tags__title', 'categories__title', 'user_id__id')  # to filter with a foreign key, field
                                                                                  # name in the related table must be
                                                                                  # written after name of the field


    def perform_create(self, serializer):
        '''Relates the created project to the logged in user.'''
        serializer.save(user_id=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)                          # defines by which fields client can search
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

