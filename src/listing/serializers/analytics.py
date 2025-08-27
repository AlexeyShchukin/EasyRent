from rest_framework import serializers


class SearchHistorySerializer(serializers.Serializer):
    """Serializer for popular search queries."""
    query = serializers.CharField()
    search_count = serializers.IntegerField()
