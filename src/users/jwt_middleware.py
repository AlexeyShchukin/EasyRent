import time
from datetime import datetime, timezone
from typing import Callable, Optional

from django.http import HttpResponse, HttpRequest
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class JWTAuthMiddleware:
    """
    Middleware to handle JWT token rotation and authentication from cookies.
    """

    refresh_window_seconds: int = 60

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def rotate_tokens(
            self, refresh_token: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        if not refresh_token:
            return None, None

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            return str(access), str(refresh)
        except TokenError:
            return None, None

    def _is_access_expiring(self, access_token: str) -> bool:
        try:
            token = AccessToken(access_token)
            exp_ts = int(token.get("exp"))
            now_ts = int(time.time())
            return exp_ts <= now_ts + self.refresh_window_seconds
        except Exception:
            return True

    def __call__(self, request: HttpRequest) -> HttpResponse:
        access_cookie = request.COOKIES.get("access")
        refresh_cookie = request.COOKIES.get("refresh")

        new_access: Optional[str] = None
        new_refresh: Optional[str] = None

        if access_cookie:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_cookie}"

            if self._is_access_expiring(access_cookie) and refresh_cookie:
                new_access, new_refresh = self.rotate_tokens(refresh_cookie)

        elif refresh_cookie:
            new_access, new_refresh = self.rotate_tokens(refresh_cookie)

        if new_access:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"

        response = self.get_response(request)

        if new_access:
            access_expiry_dt = datetime.fromtimestamp(
                AccessToken(new_access).get("exp"),
                timezone.utc
            )
            response.set_cookie(
                key="access",
                value=new_access,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=access_expiry_dt,
            )

        if new_refresh:
            refresh_expiry_dt = datetime.fromtimestamp(
                RefreshToken(new_refresh).get("exp"),
                timezone.utc
            )
            response.set_cookie(
                key="refresh",
                value=new_refresh,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=refresh_expiry_dt,
            )

        return response
