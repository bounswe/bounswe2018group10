from rest_framework import serializers

from . import models


class AcceptedProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AcceptedProject

        fields = ('id', 'user_id', 'freelancer_id', 'title', 'description', 'created_at', 'updated_at', 'tags', 'category',
                  'price', 'deadline', 'file', 'latitude', 'longitude', 'accepted_bid', 'is_done')

        extra_kwargs = {'user_id': {'read_only': True}}


class AcceptedMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcceptedMilestone
        fields = ('id', 'user_id', 'acceptedproject_id', 'description', 'amount', 'created_at', 'updated_at', 'deadline',
                  'file', 'is_done')

        extra_kwargs = {'user_id': {'read_only': True}}