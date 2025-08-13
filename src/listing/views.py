from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from src.listing.models import Listing
from src.listing.permissions import IsOwnerOrReadOnly
from src.listing.serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().select_related('owner')
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Associates the created object with the current user."""
        serializer.save(owner=self.request.user)
