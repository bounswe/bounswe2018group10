from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django_filters import rest_framework as filter


from . import serializers
from . import models
from . import permissions

# Create your views here.


class TextAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TextAnnotationSerializer
    queryset = models.TextAnnotation.objects.all()
    filter_backends = (filter.DjangoFilterBackend,)
    filter_fields = ('target__source',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateAnnotation, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageAnnotationSerializer
    queryset = models.ImageAnnotation.objects.all()
    filter_backends = (filter.DjangoFilterBackend,)
    filter_fields = ('target__source', 'target__scope')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateAnnotation, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



