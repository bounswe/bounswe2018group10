from rest_framework import serializers

from . import models

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UploadImage
        fields = ('id', 'url',)