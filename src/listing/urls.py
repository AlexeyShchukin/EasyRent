from rest_framework.routers import DefaultRouter

from src.listing.views import ListingViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet, 'listings')

urlpatterns = router.urls
