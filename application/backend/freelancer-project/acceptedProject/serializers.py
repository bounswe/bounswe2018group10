from rest_framework import serializers

from . import models


class AcceptedProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcceptedProject
        fields = ('id',
                  'user_id',
                  'freelancer_id',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'price',
                  'deadline',
                  'file',
                  'latitude',
                  'longitude',
                  'accepted_bid',
                  'is_done_client',
                  'is_done_freelancer')


class AcceptedMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcceptedMilestone
        fields = ('id', 'user_id', 'acceptedproject_id', 'description', 'amount', 'created_at', 'updated_at',
                  'deadline', 'file', 'is_done_client', 'is_done_freelancer')

        extra_kwargs = {'user_id': {'read_only': True}}


class ModelForBackendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelForBackend
        fields = ('accepted_bid',)