from django.db.models import Count
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.contrib.sessions.backends.base import UpdateError
from django.db.models.functions import Coalesce
from rest_framework.permissions import AllowAny

from src.listing.models import Listing
from src.listing.permissions import IsOwner, IsLandlordOrReadOnly
from src.listing.serializers import (
    ListingListSerializer,
    ListingCreateUpdateSerializer,
    ListingDetailSerializer
)
from src.listing.tasks import record_search_query, record_listing_view


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
    ordering_fields = ['price', 'created_at', 'reviews_count', 'rating']

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
        Calculates views for retrieve action.
        """
        queryset = self.queryset

        if self.action == 'retrieve':
            queryset = queryset.annotate(
                views_count=Count(Coalesce(
                    'views__user',
                    'views__session_id'
                ), distinct=True)
            )

        current_user = self.request.user

        is_authenticated = current_user.is_authenticated
        is_landlord = current_user.groups.filter(name="Landlord").exists()

        if is_authenticated and is_landlord:
            my_param = self.request.query_params.get("my")

            if my_param and my_param.lower() == "true":
                return queryset.filter(owner=current_user)

        return queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """Associates the created object with the current user."""
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        """Lists listings and records the search query."""
        query = request.query_params.get('search')
        if query:
            user_id = request.user.id if request.user.is_authenticated else None
            record_search_query(user_id, query)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieves a single listing and records a view."""
        instance = self.get_object()
        user_id = request.user.id if request.user.is_authenticated else None

        try:
            request.session.save()
        except UpdateError:
            request.session.create()
        session_id = request.session.session_key
        record_listing_view(user_id, str(instance.id), session_id)

        return super().retrieve(request, *args, **kwargs)
