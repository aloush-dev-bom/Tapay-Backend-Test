"""
Order Assignment views for the API application.
This module contains views for order assignment-related operations.
"""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from ..models import OrderAssignment, Order, User
from ..utils.ResponseUtils import SuccessResponse, ErrorResponse
from ..utils.ExceptionUtils import ApiExceptionHandler


class OrderAssignmentView(APIView):
    """
    API view for handling order assignment operations.
    """

    permission_classes = (permissions.IsAuthenticated,)
    
    @ApiExceptionHandler
    def post(self, request, *args, **kwargs):
        """
        Create a new order assignment and deactivate previous ones.
        
        Args:
            request: The HTTP request containing userId in body
            orderId: The ID of the order (from URL)
            
        Returns:
            Response: The created assignment details
        """
        # Get orderId from URL parameters
        orderId = kwargs.get('orderId')
        
        # Get userId from request body
        userId = request.data.get('userId')
        if not userId:
            return ErrorResponse("userId is required in request body")
        
        try:
            # Get the order and user instances
            orderInstance = Order.objects.get(pk=orderId)
            userInstance = User.objects.get(pk=userId)
            
            # Deactivate all previous assignments for this order
            OrderAssignment.objects.filter(
                order=orderInstance,
                isActive=True
            ).update(isActive=False)
            
            # Create new assignment
            assignment = OrderAssignment.objects.create(
                order=orderInstance,
                user=userInstance,
                isActive=True
            )
            
            return SuccessResponse(
                {
                    "assignmentId": assignment.id,
                    "orderId": orderId,
                    "userId": userId,
                    "assignedAt": assignment.assignedAt
                },
                message="Order assigned successfully",
                status_code=status.HTTP_201_CREATED
            )
            
        except Order.DoesNotExist:
            return ErrorResponse(f"Order with id {orderId} not found")
        except User.DoesNotExist:
            return ErrorResponse(f"User with id {userId} not found")
