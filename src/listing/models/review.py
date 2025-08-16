from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Model for user comments and ratings on a listing.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    listing = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="Reviewed listing."
    )
    renter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="The user who left the review."
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating in range from 1 to 5."
    )
    comment = models.TextField(
        blank=True,
        help_text="Comment for the listing."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('listing', 'renter')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.listing.title} by {self.renter.username}"
