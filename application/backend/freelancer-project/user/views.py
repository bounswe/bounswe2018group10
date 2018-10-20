
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import filters
from django.shortcuts import render
import json
from rest_framework.response import Response


from . import serializers
from . import models

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):

    serializer_class = AuthTokenSerializer

    def create(self, request):

        return ObtainAuthToken().post(request)



