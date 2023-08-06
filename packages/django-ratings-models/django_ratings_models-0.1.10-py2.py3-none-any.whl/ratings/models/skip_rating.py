from django.db import models
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from model_utils.models import TimeStampedModel

from ..conf import settings


class SkipRating(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        related_name='skip_rating_objects',
        on_delete=models.CASCADE)
    content_object = GenericForeignKey()
    comment = models.TextField(
        blank=True,
        null=True)
    category = models.CharField(
        max_length=250,
        blank=True,
        choices=settings.RATINGS_CATEGORIES)
    context_object_id = models.IntegerField(
        db_index=True,
        null=True)
    context_content_type = models.ForeignKey(
        ContentType,
        related_name='skip_rating_contexts',
        null=True,
        on_delete=models.CASCADE)
    context_object = GenericForeignKey(
        'context_content_type',
        'context_object_id',
    )

    class Meta:
        unique_together = [
            ('object_id', 'content_type', 'user', 'category', 'context_content_type', 'context_object_id'),
        ]

    def __str__(self):
        return '{} - {}'.format(self.category, self.user)
