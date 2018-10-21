from rest_framework import serializers

from . import models



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = models.User(
            email = validated_data['email'],
            name = validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'user_id', 'name', 'avatar', 'body', 'created_on', 'rating')
        extra_kwargs = {'user_id': {'read_only': True}}

