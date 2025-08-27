from django.db.models import Count
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.permissions import AllowAny

from src.listing.models.analytics import SearchHistory
from src.listing.models import Listing
from src.listing.serializers import (
    PopularListingSerializer,
    SearchHistorySerializer
)


class PopularListingsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PopularListingSerializer
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        queryset = (
            Listing.objects.filter(is_active=True).annotate(
                views_count=Count(Coalesce(
                    'views__user',
                    'views__session_id'
                ), distinct=True)
            ).order_by('-views_count')[:10]
        )
        return queryset


class PopularSearchesAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SearchHistorySerializer
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        return SearchHistory.objects.values('query').annotate(
            search_count=Count('query')
        ).order_by('-search_count')[:10]
