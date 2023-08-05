from django.db import models
from django.db.models import Avg

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from model_utils.models import TimeStampedModel

from ..conf import settings
from .rating import Rating
from .skip_rating import SkipRating


class OverallRating(TimeStampedModel):

    rating = models.FloatField(null=True)
    category = models.CharField(
        max_length=250, blank=True,
        choices=settings.RATINGS_CATEGORIES,
    )

    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        related_name='overall_objects',
        on_delete=models.CASCADE,
    )
    content_object = GenericForeignKey()

    context_object_id = models.IntegerField(
        db_index=True, null=True,
    )
    context_content_type = models.ForeignKey(
        ContentType,
        null=True,
        related_name='overall_contexts',
        on_delete=models.CASCADE,
    )
    context_object = GenericForeignKey(
        'context_content_type', 'context_object_id',
    )

    class Meta:
        unique_together = [
            ('context_object_id', 'context_content_type', 'category',
             'object_id', 'content_type'),
        ]

    def update(self):
        r = Rating.objects.filter(overall_rating=self).aggregate(r=Avg('rating'))['r'] or 0
        self.rating = r
        self.save()

    def user_status(self, user):
        if self.ratings.filter(user=user).exists():
            return settings.RATINGS_CH_STATUS_RATING
        elif SkipRating.objects.filter(
                category=self.category,
                user=user,
                context_object_id=self.context_object_id,
                context_content_type=self.context_content_type,
        ).exists():
            return settings.RATINGS_CH_STATUS_SKIPPED
        else:
            return settings.RATINGS_CH_STATUS_NOT_RATING
