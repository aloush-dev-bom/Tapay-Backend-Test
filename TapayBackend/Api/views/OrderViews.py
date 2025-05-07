"""
Order views for the API application.
This module contains views for order-related operations.
"""

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from ..models import Order, OrderAssignment
from ..serializers import OrderSerializer, SingleOrderSerializer
from ..utils.ResponseUtils import SuccessResponse
from ..utils.ExceptionUtils import ApiExceptionHandler


class MerchantOrdersView(APIView):
    """
    API view for handling operations on multiple orders.
    """

    permission_classes = [permissions.IsAuthenticated]
    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Get all orders for a specific merchant with optional status filtering.
        
        Args:
            request: The HTTP request containing optional status filter in query params
            merchantId: The ID of the merchant (from URL)
            
        Query Parameters:
            status (str, optional): Filter orders by status name
            
        Returns:
            Response: List of filtered orders for the merchant
        """
        merchantId = kwargs.get('merchantId')

        status = request.query_params.get('status', None)

        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('page_size', 10)

        orders = Order.objects.filter(merchant=merchantId)

        if status:
            orders = orders.filter(status__name = status)

        orders = orders.order_by('-createdAt')

        paginator = PageNumberPagination()
        paginator.page_size = pageSize
        
        paginatedOrders = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(paginatedOrders, many=True)
        
        return SuccessResponse({
            "orders": serializer.data
        }, 
        meta = {
            "total": paginator.page.paginator.count,
            "page": int(page),
            "pageSize": int(pageSize),
            "totalPages": paginator.page.paginator.num_pages,
            "hasNext": paginator.page.has_next(),
            "hasPrevious": paginator.page.has_previous()
        })

class SingleOrderView(APIView):
    """
    API view for handling operations on a single order.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Get a single order.
        
        Args:
            request: The HTTP request
            orderId: The ID of the order (from URL)
            
        Returns:
            Response: The order
        """
        merchantId = kwargs.get('merchantId')
        orderId = kwargs.get('orderId')
        orderInstance = Order.objects.get(merchant = merchantId, pk=orderId)
        
        serializer = SingleOrderSerializer(orderInstance)
        return SuccessResponse({"order": serializer.data}) 
    
class CourierOrdersView(APIView):
    """
    API view for handling operations on courier orders.
    """

    permission_classes = [permissions.IsAuthenticated]
    
    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Get all orders for a specific courier with pagination support.
        
        Args:
            request: The HTTP request
            courierId: The ID of the courier (from URL)
            page: The page number (from query params)
            page_size: The number of items per page (from query params)
            
        Returns:
            Response: Paginated list of orders with metadata
        """
        courierId = kwargs.get('courierId')
        status = request.query_params.get('status', None)
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('page_size', 10)
        
        courierOrderAssignments = OrderAssignment.objects.filter(
            user=courierId, 
            isActive=True
        )
        
        orders = Order.objects.filter(
            id__in = courierOrderAssignments.values_list('order', flat=True)
        ).order_by('createdAt') 
        
        if status:
            orders = orders.filter(status__name = status)
        
        paginator = PageNumberPagination()
        paginator.page_size = pageSize
        
        paginatedOrders = paginator.paginate_queryset(orders, request)
        
        serializer = OrderSerializer(paginatedOrders, many=True)
        
        return SuccessResponse({
            "orders": serializer.data
        }, 
        meta = {
            "total": paginator.page.paginator.count,
            "page": int(page),
            "pageSize": int(pageSize),
            "totalPages": paginator.page.paginator.num_pages,
            "hasNext": paginator.page.has_next(),
            "hasPrevious": paginator.page.has_previous()
        })
