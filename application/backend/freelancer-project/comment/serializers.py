from rest_framework import serializers

from . import models


class FreelancerCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FreelancerComment
        fields = ('id', 'user_id', 'profile_id', 'description', 'created_at', 'updated_at')

        extra_kwargs = {'user_id': {'read_only': True}}


class ClientCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClientComment
        fields = ('id', 'user_id', 'profile_id', 'description', 'created_at', 'updated_at')

        extra_kwargs = {'user_id': {'read_only': True}}