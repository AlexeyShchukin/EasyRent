from rest_framework import serializers

from src.listing.models.booking import Booking
from src.listing.serializers.listing import ListingListSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('listing', 'start_date', 'end_date')

    def validate(self, data):
        """
        Custom validation to check for overlapping bookings and dates.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "End date must be after start date or same."
            )

        listing = data.get('listing')
        if listing:
            overlapping_bookings = Booking.objects.filter(
                listing=listing,
                start_date__lte=end_date,
                end_date__gte=start_date,
                status__in=[
                    Booking.BookingStatus.PENDING,
                    Booking.BookingStatus.CONFIRMED
                ]
            ).exclude(
                id=self.instance.id if self.instance else None
            )

            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    "This listing is already booked for the selected dates."
                )

        return data


class BookingSerializer(serializers.ModelSerializer):
    listing = ListingListSerializer(read_only=True)
    renter = serializers.CharField(source='renter.username', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'listing',
            'renter',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id',)
