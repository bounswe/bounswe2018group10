from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from acceptedProject.models import AcceptedProject
from user.models import User
from . import models
from . import serializers
from . import permissions

# Create your views here.


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WalletSerializer
    queryset = models.Wallet.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateWallet, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user_id__id',)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


@api_view(['GET', 'POST'])
def payment(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)

    if request.method != 'POST':
        return Response('Only POST method is allowed!', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    saveable = serializers.PaymentSerializer(data=request.data)
    if not saveable.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    acceptedproject = saveable.validated_data['acceptedproject_id']
    amount = saveable.validated_data['amount']

    chosen_project = AcceptedProject.objects.filter(id=acceptedproject.id)
    client_id = chosen_project.values_list('user_id', flat=True)[0]
    freelancer_id = chosen_project.values_list('freelancer_id', flat=True)[0]

    client_wallet = models.Wallet.objects.get(user_id=client_id)
    if(client_wallet.budget - amount < 0):
        return Response('{message: Not enough money in the account}')
    else:
        client_wallet.budget = client_wallet.budget - amount
        client_wallet.save()

        freelancer_wallet = models.Wallet.objects.get(user_id=freelancer_id)
        freelancer_wallet.budget = freelancer_wallet.budget + amount
        freelancer_wallet.save()

        return Response('{message: Transaction completed}')