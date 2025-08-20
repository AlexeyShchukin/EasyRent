from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from rest_framework.permissions import AllowAny
from src.listing.models import Listing
from src.listing.permissions import IsOwner, IsLandlordOrReadOnly
from src.listing.serializers import (
    ListingListSerializer,
    ListingCreateUpdateSerializer,
    ListingDetailSerializer
)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.select_related('owner').all()


    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'number_of_rooms': ['gte', 'lte'],
        'location': ['exact'],
        'property_type': ['exact'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        """
        Sets permissions based on the action.
        """
        if self.action == 'create':
            self.permission_classes = [IsLandlordOrReadOnly]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner]

        else:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

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
        current_user = self.request.user

        is_authenticated = current_user.is_authenticated
        is_landlord = current_user.groups.filter(name="Landlord").exists()

        if is_authenticated and is_landlord:
            my_param = self.request.query_params.get("my")

            if my_param and my_param.lower() == "true":
                return self.queryset.filter(owner=current_user)

        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """Associates the created object with the current user."""
        serializer.save(owner=self.request.user)
