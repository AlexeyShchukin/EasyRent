from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path

from src.listing.views.booking import BookingViewSet
from src.listing.views.listing import ListingViewSet
from src.listing.views.review import ReviewViewSet

router = DefaultRouter()
router.register(r'', ListingViewSet, basename='Listings')

nested_router = NestedDefaultRouter(router, r'', lookup='listing')
nested_router.register(
    r'bookings',
    BookingViewSet,
    basename='Listing-Bookings'
)
nested_router.register(
    'reviews',
    ReviewViewSet,
    basename='listing-reviews'
)
urlpatterns = [
    path(
        'bookings/', BookingViewSet.as_view({'get': 'list'}),
        name='all-bookings'
    ),
]

urlpatterns += router.urls
urlpatterns += nested_router.urls
