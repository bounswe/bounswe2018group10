from rest_framework import serializers

from . import models
from user import serializers as user_serializers


class RefinedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RefinedBy
        fields = ('type', 'start', 'end',)


class StartEndSelectorSerializer(serializers.ModelSerializer):
    refinedBy = RefinedBySerializer()

    class Meta:
        model = models.StartEndSelector
        fields = ('type', 'value', 'refinedBy',)


class SelectorSerializer(serializers.ModelSerializer):
    startSelector = StartEndSelectorSerializer()
    endSelector = StartEndSelectorSerializer()

    class Meta:
        model = models.Selector
        fields = ('type', 'startSelector', 'endSelector',)


class FragmentSelectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FragmentSelector
        fields = ('type', 'value', 'conformsTo',)


class BodySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Body
        fields = ('value', 'language', 'type', 'format')


class TargetSerializer(serializers.ModelSerializer):
    selector = SelectorSerializer()

    class Meta:
        model = models.Target
        fields = ('source', 'selector', )


class ImageTargetSerializer(serializers.ModelSerializer):
    selector = FragmentSelectorSerializer()

    class Meta:
        model = models.ImageTarget
        fields = ('source', 'selector', 'scope', 'type')


class TextAnnotationSerializer(serializers.HyperlinkedModelSerializer):
    body = BodySerializer()
    target = TargetSerializer()
    user = user_serializers.HyperlinkedUserSerializer(read_only=True)

    class Meta:
        model = models.TextAnnotation
        fields = ('url', 'id', 'body', 'target', 'type', 'context', 'created', 'user')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = ret['url']
        ret['@context'] = ret['context']
        ret.pop('context')
        ret.pop('url')
        ret['creator'] = ret.pop('user')
        ret['creator']['nickname'] = ret['creator'].pop('username')
        ret['creator']['email'] = "mailto:" + ret['creator']['email']
        ret['creator']['type'] = "Person"
        ret['creator']['id'] = ret['creator'].pop('url')
        return ret

    def create(self, validated_data):
        body_data = validated_data.pop('body')
        target_data = validated_data.pop('target')
        selector_data = target_data.pop('selector')
        start_selector_data = selector_data.pop('startSelector')
        end_selector_data = selector_data.pop('endSelector')
        refined_by_start_sel_data = start_selector_data.pop('refinedBy')
        refined_by_end_sel_data = end_selector_data.pop('refinedBy')

        refined_by_start_sel = models.RefinedBy.objects.create(**refined_by_start_sel_data)
        refined_by_end_sel = models.RefinedBy.objects.create(**refined_by_end_sel_data)

        start_selector = models.StartEndSelector.objects.create(refinedBy=refined_by_start_sel, **start_selector_data)
        end_selector = models.StartEndSelector.objects.create(refinedBy=refined_by_end_sel, **end_selector_data)

        selector = models.Selector.objects.create(startSelector=start_selector, endSelector=end_selector, **selector_data)
        target = models.Target.objects.create(selector=selector, **target_data)
        body = models.Body.objects.create(**body_data)
        text_annotation = models.TextAnnotation.objects.create(body=body, target=target, **validated_data)
        return text_annotation


class ImageAnnotationSerializer(serializers.HyperlinkedModelSerializer):
    body = BodySerializer()
    target = ImageTargetSerializer()
    user = user_serializers.HyperlinkedUserSerializer(read_only=True)

    class Meta:
        model = models.ImageAnnotation
        fields = ('url', 'id', 'body', 'target', 'type', 'context', 'created', 'user')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # replace id with url and call it id
        ret['id'] = ret['url']
        ret.pop('url')
        # insert @ to beginning of context
        ret['@context'] = ret['context']
        ret.pop('context')
        # rename user to creator
        ret['creator'] = ret.pop('user')
        ret['creator']['nickname'] = ret['creator'].pop('username')
        ret['creator']['email'] = "mailto:" + ret['creator']['email']
        ret['creator']['type'] = "Person"
        ret['creator']['id'] = ret['creator'].pop('url')
        return ret

    def create(self, validated_data):
        body_data = validated_data.pop('body')
        target_data = validated_data.pop('target')
        selector_data = target_data.pop('selector')

        selector = models.FragmentSelector.objects.create(**selector_data)
        target = models.ImageTarget.objects.create(selector=selector, **target_data)
        body = models.Body.objects.create(**body_data)
        image_annotation = models.ImageAnnotation.objects.create(body=body, target=target, **validated_data)
        return image_annotation