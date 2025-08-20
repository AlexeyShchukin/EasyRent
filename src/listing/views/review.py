from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from src.listing.models import Review, Listing
from src.listing.permissions import IsRenter, IsReviewOwnerOrReadOnly
from src.listing.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling reviews on listings.
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        listing_pk = self.kwargs.get('listing_pk')
        return (
            Review.objects.filter(listing_id=listing_pk)
            .select_related('listing', 'renter')
        )

    def get_serializer_context(self):
        """
        Adds Listing instance to the serializer context.
        """
        context = super().get_serializer_context()
        listing_pk = self.kwargs.get('listing_pk')
        if listing_pk:
            listing = get_object_or_404(Listing, pk=listing_pk)
            context['listing'] = listing
            return context

    def perform_create(self, serializer):
        """
        Associates review with current user (renter)
        and listing id from URL.
        """
        listing = self.get_serializer_context().get('listing')
        if not listing:
            raise serializers.ValidationError(
                {"listing": "Listing ID is missing."}
            )

        serializer.save(renter=self.request.user, listing=listing)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsRenter]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsReviewOwnerOrReadOnly]
        else:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['get'])
    def my_review(self, request, listing_pk=None):
        """
        Returns user's review for specific listing.
        """
        review = self.get_queryset().filter(renter=request.user).first()
        if review:
            serializer = self.get_serializer(review)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
