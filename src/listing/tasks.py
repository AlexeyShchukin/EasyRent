from datetime import timedelta

from background_task import background
from django.utils import timezone
from django.contrib.auth.models import User

from src.listing.models.analytics import SearchHistory, ViewHistory


@background(schedule=0)
def record_listing_view(user_id: int | None, listing_id: str, session_id: str):
    """Records unique views per user id or per session if not authenticated."""
    one_day_ago = timezone.now() - timedelta(days=1)

    if user_id:
        viewed_by_user = ViewHistory.objects.filter(
            user_id=user_id,
            listing_id=listing_id,
            viewed_at__gte=one_day_ago
        ).exists()

        if viewed_by_user:
            return

    elif session_id:
        viewed_by_session = ViewHistory.objects.filter(
            session_id=session_id,
            listing_id=listing_id,
            viewed_at__gte=one_day_ago
        ).exists()

        if viewed_by_session:
            return

    ViewHistory.objects.create(user_id=user_id, listing_id=listing_id, session_id=session_id)


@background(schedule=0)
def record_search_query(user_id: int | None, query: str):
    normalized_query = _normalize_query(query)
    user = User.objects.get(id=user_id) if user_id else None
    SearchHistory.objects.create(user=user, query=normalized_query)


def _normalize_query(query: str) -> str:
    waste = {'for', 'in', 'the', 'a', ',', '-'}
    normalized_words = query.lower().split()
    print(normalized_words)
    filtered_words = [
        word.strip(', .-') for word in normalized_words if word not in waste
    ]
    sorted_words = sorted(filtered_words)
    return " ".join(sorted_words)
