from rest_framework import serializers

from ...models import SkipRating


class SkipRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkipRating
        fields = [
            'object_id',
            'content_type',
            'comment',
            'category',
            'context_object_id',
            'context_content_type',
        ]

    def create(self, validated_data):
        return SkipRating.objects.create(**validated_data)
