from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from src.listing.models import Listing
from src.listing.permissions import IsOwnerOrReadOnly, IsLandlordOrReadOnly
from src.listing.serializers import (
    ListingListSerializer,
    ListingCreateUpdateSerializer,
    ListingDetailSerializer
)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().select_related('owner')
    permission_classes = [IsLandlordOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'number_of_rooms': ['gte', 'lte'],
        'location': ['exact'],
        'property_type': ['exact'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListingListSerializer
        if self.action == 'retrieve':
            return ListingDetailSerializer
        return ListingCreateUpdateSerializer

    def get_queryset(self):
        """
        If query param 'my' is present and True,
        return only the current user's listings.
        """
        queryset = super().get_queryset()
        current_user = self.request.user

        is_authenticated = current_user.is_authenticated
        is_landlord = current_user.groups.filter(name="Landlord").exists()

        if is_authenticated and is_landlord:
            my_param = self.request.query_params.get("my")
            if my_param and my_param.lower() == "true":
                return queryset.filter(owner=current_user)

        return queryset

    def perform_create(self, serializer):
        """Associates the created object with the current user."""
        serializer.save(owner=self.request.user)
