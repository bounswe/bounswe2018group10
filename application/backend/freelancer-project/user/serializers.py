from rest_framework import serializers

from . import models



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password', 'username')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = models.User(
            email = validated_data['email'],
            name = validated_data['name'],
            username = validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientProfile
        fields = ('id', 'user_id', 'avatar', 'body')

    def create(self, validated_data):
        client_profile = models.ClientProfile(
            user_id = validated_data["user_id"],
            avatar = validated_data["avatar"],
            body = validated_data["body"],
        )

        client_profile.save()


class FreelancerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FreelancerProfile
        fields = ('id', 'user_id', 'avatar', 'body')

    def create(self, validated_data):
        freelancer_profile = models.ClientProfile(
            user_id = validated_data["user_id"],
            avatar = validated_data["avatar"],
            body = validated_data["body"],
        )

        freelancer_profile.save()


