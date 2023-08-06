from django.db import models
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from model_utils.models import TimeStampedModel


class Interaction(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='interactions',
        on_delete=models.CASCADE,
    )
    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        related_name='interaction_objects',
        on_delete=models.CASCADE,
    )
    target_object = GenericForeignKey()

    ratings = models.ManyToManyField(
        'OverallRating',
        related_name='interactions')
    rating = models.FloatField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.target_object)

    def update(self):
        r = self.ratings.all().aggregate(r=models.Avg('rating'))['r'] or 0
        self.rating = round(r, 1)
        self.save()
        try:
            self.target_object.stats.get('rating').set(self.rating)
        except AttributeError:
            pass
