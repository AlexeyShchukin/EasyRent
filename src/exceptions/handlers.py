import logging
import traceback

from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from src.exceptions.exceptions import ErrorType

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, APIException) and hasattr(exc, "error_type"):
        return Response(
            {
                "detail": exc.detail,
                "error_type": exc.error_type.value
            },
            status=exc.status_code
        )

    if isinstance(exc, DRFValidationError):
        return Response(
            {
                "detail": exc.detail,
                "error_type": ErrorType.VALIDATION_ERROR.value
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                "detail": str(exc),
                "error_type": ErrorType.VALIDATION_ERROR.value
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, IntegrityError):
        return Response(
            {
                "detail": str(exc),
                "error_type": ErrorType.INTEGRITY_ERROR.value
            },
            status=status.HTTP_400_BAD_REQUEST
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
