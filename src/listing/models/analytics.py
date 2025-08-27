from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models


class SearchHistory(models.Model):
    """
    Model to store user search queries.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='search_queries',
        null=True
    )
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Search History"
        verbose_name_plural = "Search History"


class ViewHistory(models.Model):
    """
    Model to track views for listings.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='viewed_listings',
        null=True
    )
    listing = models.ForeignKey(
        'listing.Listing',
        on_delete=models.CASCADE,
        related_name='views'
    )
    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = "View History"
        verbose_name_plural = "View History"
