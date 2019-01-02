from rest_framework import serializers

from . import models
from payment import models as payment_models
from acceptedProject import models as acceptedProject_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password', 'username', 'role',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = models.User(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['username'],
            role=validated_data['role'],
        )

        user.set_password(validated_data['password'])
        user.save()

        profile = models.FreelancerProfile(user=user)
        profile.save()
        profile = models.ClientProfile(user=user)
        profile.save()

        wallet = payment_models.Wallet(user_id=user)
        wallet.save()

        return user


class ClientProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = models.ClientProfile
        fields = ('id', 'user', 'avatar', 'body', 'user_info', 'tags',)

    def create(self, validated_data):
        client_profile = models.ClientProfile(
            user=validated_data["user"],
            avatar=validated_data["avatar"],
            body=validated_data["body"],
            tags=validated_data["tags"],
        )

        client_profile.save()

        return client_profile

    def get_user_info(self,obj):
        return UserSerializer(obj.user).data


class FreelancerProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = models.FreelancerProfile
        fields = ('id', 'user', 'avatar', 'body', 'user_info', 'tags', )

    def create(self, validated_data):
        freelancer_profile = models.FreelancerProfile(
            user=validated_data["user"],
            avatar=validated_data["avatar"],
            body=validated_data["body"],
            tags=validated_data["tags"],
        )

        freelancer_profile.save()

        return freelancer_profile

    def get_user_info(self,obj):
        return UserSerializer(obj.user).data