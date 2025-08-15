from datetime import date

from rest_framework import serializers

from src.listing.models.booking import Booking
from src.listing.serializers.listing import ListingListSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    listing = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ('listing', 'start_date', 'end_date')

    def validate(self, data):
        """
        Custom validation to check for overlapping bookings and dates.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        current_date = date.today()

        if start_date < current_date:
            raise serializers.ValidationError(
                {"start_date": "Start date cannot be in the past."}
            )

        if start_date > end_date:
            raise serializers.ValidationError(
                "End date must be after start date or same."
            )

        listing = self.context.get('listing')

        if not listing:
            raise serializers.ValidationError(
                {"listing": "Listing object not provided in context."}
            )

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
            'renter',
            'start_date',
            'end_date',
            'status',
            'listing'
        )
        read_only_fields = ('id',)
