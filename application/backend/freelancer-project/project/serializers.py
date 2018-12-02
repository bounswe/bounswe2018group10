from rest_framework import serializers

from . import models
from user import models as userModels


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


class BidSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.Bid
        fields = ('id', 'user_id', 'project_id', 'description', 'amount', 'created_at', 'updated_at', 'avatar', 'name')

        extra_kwargs = {'user_id': {'read_only': True}}

    def get_avatar(self,obj):
        request = self.context.get('request')
        avatar = userModels.FreelancerProfile.objects.get(id=obj.user_id.id).avatar
        if avatar:
            return request.build_absolute_uri(avatar.url)
        else:
            return None

    def get_name(self,obj):
        return obj.user_id.name


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Milestone
        fields = ('id', 'user_id', 'bid_id', 'description', 'amount', 'created_at', 'updated_at', 'deadline')

        extra_kwargs = {'user_id': {'read_only': True}}
