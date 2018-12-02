from rest_framework import serializers

from . import models


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = ('id', 'user_id', 'budget')

        extra_kwargs = {'user_id': {'read_only': True}}


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = ('acceptedproject_id', 'amount')

