from rest_framework import serializers

from django.contrib.auth import get_user_model

from ...models import OverallRating, Rating


class UserSerializer(serializers.ModelSerializer):
    shortName = serializers.CharField(source='short_name')
    fullName = serializers.CharField(source='full_name')

    class Meta:
        model = get_user_model()
        fields = [
            'pk',
            'shortName',
            'email',
            'fullName',
        ]


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rating
        fields = [
            'pk',
            'rating',
            'comment',
            'category',
            'user',
        ]


class OverallRatingSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True)
    userStatus = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = OverallRating
        fields = [
            'pk',
            'rating',
            'category',
            'ratings',
            'userStatus',
        ]

    def get_userStatus(self, obj):
        user = self.context.get('request').user
        return obj.user_status(user)

    def get_category(self, obj):
        return obj.category.upper().replace('-', '_')
