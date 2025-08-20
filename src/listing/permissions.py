from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsLandlordOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        is_landlord = user.groups.filter(name='Landlord').exists()
        return user.is_authenticated and is_landlord


class IsOwnerOfBookingListing(permissions.BasePermission):
    """
    Allows only the landlord of a listing to perform actions.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_landlord = user.groups.filter(name='Landlord').exists()

        if is_landlord:
            return obj.listing.owner == user
        return False


class IsRenter(permissions.BasePermission):
    """
    Allow renters to perform actions.
    """

    def has_permission(self, request, view):
        user = request.user
        is_renter = user.groups.filter(name='Renter').exists()
        return user.is_authenticated and is_renter


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows only the renter who left the review to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.renter == request.user
