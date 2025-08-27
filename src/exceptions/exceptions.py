from enum import Enum

from rest_framework.exceptions import APIException
from rest_framework import status


class ErrorType(str, Enum):
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    PERMISSION_ERROR = "permission_error"
    AUTHENTICATION_ERROR = "authentication_error"
    INVALID_STATUS = "invalid_status"
    UNKNOWN_ERROR = "unknown_error"
    INTEGRITY_ERROR = "integrity_error"


class BookingStatusError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The booking status does not allow this action.'
    default_code = 'invalid_booking_status'
    error_type = ErrorType.INVALID_STATUS


class BookingOwnershipError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action on this booking.'
    default_code = 'permission_denied'
    error_type = ErrorType.PERMISSION_ERROR


class BookingRelationshipError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The booking does not belong to the specified listing.'
    default_code = 'invalid_relationship'
    error_type = ErrorType.VALIDATION_ERROR
