from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework import views
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action

from . import serializers
from . import models
from . import permissions


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateUser,)


class LoginViewSet(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request, **kwargs):
        return ObtainAuthToken().post(request)


class ProfileViewSet(viewsets.ModelViewSet):
 #   serializer_class = serializers.ProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__id', 'name',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            return models.FreelancerProfile.objects.filter(user_id=user.id)
        return models.ClientProfile.objects.filter(user_id=user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        user = self.request.user
        if user.role == user.FREELANCER:
            return serializers.FreelancerProfileSerializer
        elif user.role == user.CLIENT:
            return serializers.ClientProfileSerializer
        else:
            return None


class ClientProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientProfileSerializer
    queryset = models.ClientProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__id', 'name',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateClientProfile,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class FreelancerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FreelancerProfileSerializer
    queryset = models.FreelancerProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__id', 'name',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateFreelancerProfile,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ChangeProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChangeProfileSerializer
    queryset = models.User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateUser,)

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        if instance.role == instance.FREELANCER:
            instance.role = instance.CLIENT
        else:
            instance.role = instance.FREELANCER

        instance.save(update_fields=['role'])
        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

