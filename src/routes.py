from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include

from src.listing.views.analytics import PopularListingsAPIView, PopularSearchesAPIView
from src.listing.views.booking import BookingViewSet
from src.listing.views.listing import ListingViewSet
from src.listing.views.review import ReviewViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listings')
router.register(r'bookings', BookingViewSet, basename='bookings')

listings_router = NestedDefaultRouter(router, r'listings', lookup='listing')
listings_router.register(r'reviews', ReviewViewSet, basename='listing-reviews')
listings_router.register(r'bookings', BookingViewSet, basename='listing-bookings')

urlpatterns = [
    path('listings/popular/', PopularListingsAPIView.as_view(), name='popular-listings'),
    path('listings/popular-searches/', PopularSearchesAPIView.as_view(), name='popular-searches'),
    path('', include(router.urls)),
    path('', include(listings_router.urls)),
    path('users/', include('src.users.urls')),
]
