from django.db import models
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from model_utils.models import TimeStampedModel

from ..conf import settings


class Rating(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=250,
        blank=True,
        choices=settings.RATINGS_CATEGORIES,
    )
    overall_rating = models.ForeignKey(
        'OverallRating',
        null=True,
        related_name='ratings',
        on_delete=models.CASCADE,
    )

    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        related_name='rating_objects',
        on_delete=models.CASCADE,
    )
    content_object = GenericForeignKey()

    context_object_id = models.IntegerField(
        db_index=True, null=True,
    )
    context_content_type = models.ForeignKey(
        ContentType,
        null=True,
        related_name='rating_contexts',
        on_delete=models.CASCADE,
    )
    context_object = GenericForeignKey(
        'context_content_type', 'context_object_id',
    )

    class Meta:
        unique_together = [
            ('object_id', 'content_type', 'user', 'category',
             'context_content_type', 'context_object_id'), ]

    def __str__(self):
        return str(self.rating)

    def clear(self):
        overall = self.overall_rating
        self.delete()
        overall.update()
        return overall.rating

    @classmethod
    def update(
            cls, rating_context, user, rating, category='', comment=None,
            rating_object=None):

        # @@@ Still doing too much in this method
        from .overall_rating import OverallRating
        rated_object = rating_object

        rating_context_ct = ContentType.objects.get_for_model(rating_context)
        rate_objects = cls.objects.filter(
            context_object_id=rating_context.pk,
            context_content_type_id=rating_context_ct.pk,
            user=user,
            category=category,
        )
        if rated_object:
            rated_object_ct = ContentType.objects.get_for_model(rated_object)
            rate_objects = rate_objects.filter(
                object_id=rated_object.pk,
                content_type=rated_object_ct,
            )
        rate_obj = rate_objects.first()

        if rate_obj and rating == 0:
            return rate_obj.clear()

        if rate_obj is None:
            rate_obj = cls.objects.create(
                context_object_id=rating_context.pk,
                context_content_type_id=rating_context_ct.pk,
                user=user,
                category=category,
                rating=rating,
                comment=comment,
            )
            if rated_object:
                rate_obj.content_object = rated_object
                rate_obj.save()

        kwargs = {
            'context_object_id': rating_context.pk,
            'context_content_type_id': rating_context_ct.pk,
            'category': category,
        }
        if rated_object:
            kwargs.update({
                'object_id': rated_object.pk,
                'content_type_id': rated_object_ct.pk,
            })

        overall, _ = OverallRating.objects.get_or_create(**kwargs)
        rate_obj.overall_rating = overall
        rate_obj.rating = rating
        rate_obj.save()

        overall.update()

        return overall.rating
