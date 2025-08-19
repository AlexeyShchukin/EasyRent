from rest_framework import serializers

from src.listing.models import Listing


class ListingDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = (
            'id',
            'title',
            'description',
            'location',
            'price',
            'number_of_rooms',
            'property_type',
            'is_active',
            'rating',
            'reviews_count',
            'owner_username',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class ListingListSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = (
            'id',
            'title',
            'price',
            'location',
            'rating',
            'reviews_count',
            'number_of_rooms',
            'owner_username',
            'is_active'
        )
        read_only_fields = ('id',)


class ListingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = (
            'title',
            'description',
            'location',
            'price',
            'number_of_rooms',
            'property_type',
            'is_active',
        )
