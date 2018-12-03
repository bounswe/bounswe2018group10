from rest_framework import serializers

from . import models
from user import serializers as userSerializers
from user import models as userModels


class FreelancerCommentSerializer(serializers.ModelSerializer):
    user_id = userSerializers.UserSerializer(read_only=True)
    commenter_avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.FreelancerComment
        fields = ('id', 'user_id', 'profile_id', 'description', 'created_at', 'updated_at', 'commenter_avatar',)

        extra_kwargs = {'user_id': {'read_only': True}}

    def get_commenter_avatar(self,obj):
        request = self.context.get('request')
        avatar = userModels.ClientProfile.objects.get(id=obj.user_id.id).avatar
        if avatar:
            return request.build_absolute_uri(avatar.url)
        else:
            return None


class ClientCommentSerializer(serializers.ModelSerializer):
    user_id = userSerializers.UserSerializer(read_only=True)
    commenter_avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.ClientComment
        fields = ('id', 'user_id', 'profile_id', 'description', 'created_at', 'updated_at', 'commenter_avatar',)

        extra_kwargs = {'user_id': {'read_only': True}}

    def get_commenter_avatar(self,obj):
        request = self.context.get('request')
        avatar = userModels.ClientProfile.objects.get(id=obj.user_id.id).avatar
        if avatar:
            return request.build_absolute_uri(avatar.url)
        else:
            return None
