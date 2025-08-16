import logging
import traceback

from django.conf import settings
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from src.exceptions.exceptions import (
    BookingOwnershipError,
    BookingStatusError,
    ErrorType,
    BookingRelationshipError
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, BookingRelationshipError):
        return Response(
            {
                'detail': str(exc),
                'error_type': ErrorType.VALIDATION_ERROR.value
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, BookingOwnershipError):
        return Response(
            {
                'detail': str(exc),
                'error_type': ErrorType.PERMISSION_ERROR.value
            },
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, BookingStatusError):
        return Response(
            {
                'detail': str(exc),
                'error_type': ErrorType.INVALID_STATUS.value
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if response:
        error_type = ErrorType.UNKNOWN_ERROR
        if response.status_code == 400:
            error_type = ErrorType.VALIDATION_ERROR
        elif response.status_code == 404:
            error_type = ErrorType.NOT_FOUND
        elif response.status_code == 403:
            error_type = ErrorType.PERMISSION_ERROR

        response.data['error_type'] = error_type.value
        return response

    if settings.DEBUG:
        return Response(
            {
                'detail': traceback.format_exc(),
                'error_type': ErrorType.UNKNOWN_ERROR.value
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    logger.error(f"Unknown server error: {exc}", exc_info=True)

    return Response(
        {
            'detail': 'A server error occurred.',
            'error_type': ErrorType.UNKNOWN_ERROR.value
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
