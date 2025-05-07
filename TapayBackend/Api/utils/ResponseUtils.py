"""
Response utilities for the API application.
This module contains utility functions for creating consistent API responses.
"""

from rest_framework.response import Response
from rest_framework import status


def SuccessResponse(data, message=None, meta=None, status_code=status.HTTP_200_OK):
    """
    Create a success response with consistent format.
    
    Args:
        data: The data to include in the response
        message: Optional success message
        status_code: HTTP status code (default: 200)
        
    Returns:
        Response: A DRF Response object with consistent format
    """
    response_data = {"data": data}
    if message:
        response_data["message"] = message

    if meta:
        response_data["meta"] = meta
        
    return Response(response_data, status=status_code)


def ErrorResponse(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None):
    """
    Create an error response with consistent format.
    
    Args:
        message: Error message
        status_code: HTTP status code (default: 400)
        errors: Optional detailed error information
        
    Returns:
        Response: A DRF Response object with consistent format
    """
    response_data = {"error": message}
    if errors:
        response_data["errors"] = errors
    return Response(response_data, status=status_code) 