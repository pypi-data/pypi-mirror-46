from django.contrib import admin

from . import models


class InteractionAdmin(admin.ModelAdmin):
    list_filter = ('content_type', )
    list_display = (
        'user',
        'content_type', 'target_object', 'object_id',
        'rating',
        'created', 'modified',
    )


class OverallRatingAdmin(admin.ModelAdmin):
    list_filter = ('content_type', )
    list_display = (
        'rating', 'category', 'context_object',
        'created', 'modified',
    )


class RatingAdmin(admin.ModelAdmin):
    list_filter = ('content_type', )
    list_display = (
        'user', 'rating', 'category',
        'content_type', 'content_object', 'context_object',
        'created', 'modified',
    )


class SkipRatingAdmin(admin.ModelAdmin):
    list_filter = ('content_type', )
    list_display = (
        'user', 'category',
        'content_type', 'content_object', 'context_object',
        'created', 'modified',
    )


admin.site.register(models.Interaction, InteractionAdmin)
admin.site.register(models.OverallRating, OverallRatingAdmin)
admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.SkipRating, SkipRatingAdmin)
