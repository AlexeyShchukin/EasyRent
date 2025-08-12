from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model


class Listing(models.Model):
    class PropertyType(models.TextChoices):
        APARTMENT = 'APARTMENT', 'Apartment'
        HOUSE = 'HOUSE', 'House'
        CONDO = 'CONDO', 'Condo'
        VILLA = 'VILLA', 'Villa'

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    number_of_rooms = models.PositiveSmallIntegerField()
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='listings'
    )

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.title} by {self.owner.username}'
