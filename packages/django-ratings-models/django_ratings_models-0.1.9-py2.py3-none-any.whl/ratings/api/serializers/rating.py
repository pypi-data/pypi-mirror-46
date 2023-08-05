from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType

from ...models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = [
            'object_id',
            'content_type',
            'rating',
            'comment',
            'category',
            'context_object_id',
            'context_content_type',
        ]

    def create(self, validated_data):
        user = validated_data.get('user')
        context_object_id = validated_data.get('context_object_id')
        context_content_type = validated_data.get('context_content_type')
        content_type = validated_data.get('content_type')
        object_id = validated_data.get('object_id')
        rating_object = None

        ct = ContentType.objects.get_for_id(context_content_type)
        rating_context = ct.get_object_for_this_type(pk=context_object_id)

        if object_id:
            ct = ContentType.objects.get_for_id(content_type)
            rating_object = ct.get_object_for_this_type(pk=object_id)

        return Rating.update(
            rating_context,
            user,
            validated_data.get('rating'),
            validated_data.get('category'),
            validated_data.get('comment'),
            rating_object,
        )
