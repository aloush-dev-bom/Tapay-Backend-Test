"""
Exception utilities for the API application.
This module contains utility functions and decorators for exception handling.
"""

import functools
import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from .ResponseUtils import ErrorResponse

logger = logging.getLogger(__name__)


def ApiExceptionHandler(func):
    """
    Decorator to handle exceptions in API views.
    
    Args:
        func: The view method to decorate
        
    Returns:
        The decorated function that handles exceptions
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist as e:
            logger.warning(f"Object not found: {str(e)}")
            return ErrorResponse(
                message="The requested resource was not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            logger.warning(f"Value error: {str(e)}")
            return ErrorResponse(str(e))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return ErrorResponse(
                message="An unexpected error occurred",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper 