from rest_framework import serializers

from . import models


class ProjectSerializer(serializers.ModelSerializer):
    '''Defines serializer which converts json request to python objects and vice versa.'''

    class Meta:
        model = models.Project                           # sets the model which will be used for this serializer

        fields = ('id', 'user_id', 'title', 'description', 'created_at', 'updated_at', 'tags', 'category',
                  'budget_min', 'budget_max', 'deadline', 'file', 'latitude', 'longitude')

        extra_kwargs = {'user_id': {'read_only': True}}  # sets user_id to read_only thus user can't assign a value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'title')                        # lists the fields which will be shown is json response


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'title')