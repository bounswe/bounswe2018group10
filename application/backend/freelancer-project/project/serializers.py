from rest_framework import serializers

from . import models


class ProjectSerializer(serializers.ModelSerializer):
    '''Defines serializer which converts json request to python objects and vice versa.'''

    class Meta:
        model = models.Project                           # sets the model which will be used for this serializer

        fields = ('id', 'user_id', 'title', 'description', 'created_at', 'updated_at', 'tags', 'category',
                  'budget_min', 'budget_max', 'deadline', 'file', 'latitude', 'longitude', 'accepted_bid')

        extra_kwargs = {'user_id': {'read_only': True}}  # sets user_id to read_only thus user can't assign a value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'title')                        # lists the fields which will be shown is json response


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'title')


class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bid
        fields = ('id', 'user_id', 'project_id', 'description', 'amount', 'created_at', 'updated_at')

        extra_kwargs = {'user_id': {'read_only': True}}


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Milestone
        fields = ('id', 'user_id', 'bid_id', 'description', 'amount', 'created_at', 'updated_at', 'deadline')

        extra_kwargs = {'user_id': {'read_only': True}}