from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password', 'username',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = models.User(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        profile = models.FreelancerProfile(user=user)
        profile.save()
        profile = models.ClientProfile(user=user)
        profile.save()
        return user


class ClientProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = models.ClientProfile
        fields = ('id', 'user', 'avatar', 'body', 'user_info',)

    def create(self, validated_data):
        client_profile = models.ClientProfile(
            user=validated_data["user"],
            avatar=validated_data["avatar"],
            body=validated_data["body"],
        )

        client_profile.save()

        return client_profile

    def get_user_info(self,obj):
        return UserSerializer(obj.user).data


class FreelancerProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = models.FreelancerProfile
        fields = ('id', 'user', 'avatar', 'body', 'user_info',)

    def create(self, validated_data):
        freelancer_profile = models.FreelancerProfile(
            user=validated_data["user"],
            avatar=validated_data["avatar"],
            body=validated_data["body"],
        )

        freelancer_profile.save()

        return freelancer_profile

    def get_user_info(self,obj):
        return UserSerializer(obj.user).data
