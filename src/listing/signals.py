from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.listing.models import Review, Listing


@receiver(post_save, sender=Review)
def update_listing_rating(sender, instance, created, **kwargs):
    """
    Updates the listing's rating and reviews count
    whenever a review is saved.
    """
    listing = instance.listing

    aggregated_data = (
        Review
        .objects
        .filter(listing=listing)
        .aggregate(
            avg_rating=Avg('rating'),
            count_reviews=Count('id')
        )
    )

    avg_rating = aggregated_data['avg_rating']
    reviews_count = aggregated_data['count_reviews']

    listing.rating = round(avg_rating, 2) if avg_rating is not None else 0.00
    listing.reviews_count = reviews_count
    listing.save()
