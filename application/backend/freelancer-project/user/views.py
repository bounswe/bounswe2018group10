
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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


class LoginViewSet(viewsets.ViewSet):

    serializer_class = AuthTokenSerializer

    def create(self, request):

        return ObtainAuthToken().post(request)


class ClientProfileViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ClientProfileSerializer
    queryset = models.ClientProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user_id__id', 'name',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateClientProfile, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class FreelancerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FreelancerProfileSerializer
    queryset = models.FreelancerProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user_id__id', 'name',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateFreelancerProfile, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)