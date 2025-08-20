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

CUSTOM_ERROR_MAPPING = {
    BookingRelationshipError: (
        status.HTTP_400_BAD_REQUEST,
        ErrorType.VALIDATION_ERROR
    ),
    BookingStatusError: (
        status.HTTP_400_BAD_REQUEST,
        ErrorType.INVALID_STATUS
    ),
    BookingOwnershipError: (
        status.HTTP_403_FORBIDDEN,
        ErrorType.PERMISSION_ERROR
    ),
}


def custom_exception_handler(exc, context):
    if type(exc) in CUSTOM_ERROR_MAPPING:
        http_status, error_type = CUSTOM_ERROR_MAPPING[type(exc)]
        return Response(
            {
                'detail': str(exc),
                'error_type': error_type.value
            },
            status=http_status
        )

    response = exception_handler(exc, context)
    if response:
        status_to_error_type = {
            400: ErrorType.VALIDATION_ERROR,
            401: ErrorType.AUTHENTICATION_ERROR,
            403: ErrorType.PERMISSION_ERROR,
            404: ErrorType.NOT_FOUND,
        }
        response.data['error_type'] = status_to_error_type.get(
            response.status_code, ErrorType.UNKNOWN_ERROR
        ).value
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
