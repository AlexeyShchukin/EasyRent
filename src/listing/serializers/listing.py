from rest_framework import serializers

from src.listing.models import Listing


class ListingDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

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

    class Meta:
        model = Listing
        fields = (
            'id',
            'title',
            'price',
            'location',
            'number_of_rooms',
            'owner_username',
        )
        read_only_fields = ('id', 'owner_username')


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
