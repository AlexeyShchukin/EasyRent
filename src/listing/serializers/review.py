from rest_framework import serializers

from src.listing.models import Review, Booking


class ReviewSerializer(serializers.ModelSerializer):
    renter_username = serializers.CharField(
        source='renter.username',
        read_only=True
    )
    listing_title = serializers.CharField(
        source='listing.title',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'listing_title',
            'renter_username',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        """
        Validate that the user has a completed booking for this listing.
        """
        current_user = self.context['request'].user
        current_listing = self.context['listing']

        has_completed_booking = Booking.objects.filter(
            listing=current_listing,
            renter=current_user,
            status=Booking.BookingStatus.COMPLETED
        ).exists()

        if not has_completed_booking:
            raise serializers.ValidationError(
                "You can leave a review only after completed booking."
            )
        return attrs
