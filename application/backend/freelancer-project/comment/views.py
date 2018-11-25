from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters


from . import serializers
from . import models
from . import permissions

# Create your views here.


class FreelancerCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FreelancerCommentSerializer
    queryset = models.FreelancerComment.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=profile_id__id',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateComment, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ClientCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientCommentSerializer
    queryset = models.ClientComment.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=profile_id__id',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateComment, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


