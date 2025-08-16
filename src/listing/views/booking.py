from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers

from src.exceptions.exceptions import (
    BookingOwnershipError,
    BookingStatusError,
    BookingRelationshipError
)
from src.listing.models import Booking, Listing
from src.listing.permissions import IsRenter, IsOwnerOfBookingListing
from src.listing.serializers import BookingSerializer, BookingCreateSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related(
        'listing',
        'renter'
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def get_permissions(self):
        """
        Sets permissions based on the action and user role.
        """
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]

        elif self.action in ['create', 'cancel']:
            self.permission_classes = [IsRenter]

        elif self.action in ['confirm', 'reject']:
            self.permission_classes = [
                IsAuthenticated,
                IsOwnerOfBookingListing
            ]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        """
        Prevents direct modification of the booking status.
        """
        if 'status' in serializer.validated_data:
            raise serializers.ValidationError(
                {'status': 'Booking status cannot be updated directly.'}
            )
        serializer.save()

    def get_queryset(self):
        """
        Filters bookings based on user role.
        Landlords can see bookings for their listings.
        Renters can see their own bookings.
        """
        user = self.request.user

        listing_pk = self.kwargs.get('listing_pk')

        if user.is_authenticated:
            if user.groups.filter(name='Renter').exists():
                return self.queryset.filter(renter=user)

            if user.groups.filter(name='Landlord').exists():
                if listing_pk:
                    return self.queryset.filter(
                        listing_id=listing_pk,
                        listing__owner=user
                    )
                return self.queryset.filter(listing__owner=user)

        return self.queryset.none()

    def get_serializer_context(self):
        """
        Allows the serializer's validate() method
        to access the Listing instance.
        """
        context = super().get_serializer_context()
        if self.action == 'create':
            listing_id = self.kwargs.get('listing_pk')
            if listing_id:
                listing = get_object_or_404(Listing, pk=listing_id)
                context['listing'] = listing
        return context

    def perform_create(self, serializer):
        """
        Associates booking with current user (renter)
        and listing id from URL.
        """
        listing = self.get_serializer_context().get('listing')
        if not listing:
            raise serializers.ValidationError(
                {"listing": "Listing ID is missing."}
            )

        serializer.save(
            renter=self.request.user,
            listing=listing,
            status=Booking.BookingStatus.PENDING
        )

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None, listing_pk=None):
        """
        Allows a renter to cancel their booking.
        """
        booking = self.get_object()

        self._validate_relationship(booking, listing_pk)

        if booking.renter != request.user:
            raise BookingOwnershipError(
                "You do not have permission to cancel this booking."
            )

        if booking.status not in [
            Booking.BookingStatus.PENDING,
            Booking.BookingStatus.CONFIRMED
        ]:
            raise BookingStatusError(
                "Only pending or confirmed bookings can be cancelled."
            )

        current_date = date.today()
        time_to_checkin = (booking.start_date - current_date).days
        if time_to_checkin < 2:
            raise BookingStatusError(
                "Booking cannot be cancelled less than 2 days before check-in."
            )

        booking.status = Booking.BookingStatus.CANCELLED
        booking.save()
        return Response(
            {'detail': 'Booking cancelled successfully.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None, listing_pk=None):
        """
        Allows a landlord to confirm a booking.
        """
        booking = self.get_object()

        self._validate_relationship(booking, listing_pk)
        if booking.status != Booking.BookingStatus.PENDING:
            raise BookingStatusError("Only pending bookings can be confirmed.")

        booking.status = Booking.BookingStatus.CONFIRMED
        booking.save()
        return Response(
            {'detail': 'Booking confirmed successfully.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None, listing_pk=None):
        """
        Allows a landlord to reject a booking.
        """
        booking = self.get_object()

        self._validate_relationship(booking, listing_pk)

        if booking.status != Booking.BookingStatus.PENDING:
            raise BookingStatusError(
                "Only pending bookings can be confirmed."
            )

        booking.status = Booking.BookingStatus.REJECTED
        booking.save()
        return Response(
            {'detail': 'Booking rejected successfully.'},
            status=status.HTTP_200_OK
        )

    def _validate_relationship(self, booking, listing_pk):
        """
        Ensure the given booking is associated  with the specified listing.
        """
        if str(booking.listing.id) != listing_pk:
            raise BookingRelationshipError(
                "Booking does not belong to this listing."
            )
