from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from Api.models import Merchant, User
from Api.serializers import MerchantSerializer, CourierSerializer
from ..utils.ResponseUtils import SuccessResponse
from ..utils.ExceptionUtils import ApiExceptionHandler

class MerchantsView(APIView):
    """
    API view for managing merchants in the system.
    Provides endpoints for listing all merchants and creating new merchant accounts.
    Requires authentication for all operations.
    """
    permission_classes = [IsAuthenticated]

    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Retrieves a paginated list of all merchants in the system.
        
        Query Parameters:
            page (int): The page number to retrieve (default: 1)
            page_size (int): Number of items per page (default: 10)
            
        Returns:
            Response: A paginated list of merchants with metadata about the pagination
        """
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('page_size', 10)

        merchants = Merchant.objects.all().order_by('-createdAt')

        paginator = PageNumberPagination()
        paginator.page_size = pageSize

        paginatedMerchants = paginator.paginate_queryset(merchants, request)

        serializer = MerchantSerializer(paginatedMerchants, many=True)

        return SuccessResponse({
            "merchants": serializer.data
        }, 
        meta = {
            "total": paginator.page.paginator.count,
            "page": int(page),
            "pageSize": int(pageSize),
            "totalPages": paginator.page.paginator.num_pages,
            "hasNext": paginator.page.has_next(),
            "hasPrevious": paginator.page.has_previous()
        })
        
    @ApiExceptionHandler
    def post(self, request, *args, **kwargs):
        """
        Creates a new merchant account in the system.
        
        Request Body:
            name (str): Name of the merchant
            contactEmail (str): Contact email of the merchant
            contactPhone (str): Contact phone number of the merchant
            address (str): Physical address of the merchant
            
        Returns:
            Response: The created merchant data with a success message
        """
        data = request.data

        merchantInstance = Merchant.objects.create(
            name=data['name'],
            contactEmail=data['contactEmail'],
            contactPhone=data['contactPhone'],
            address=data['address'],
        )

        merchantInstance.save()

        serializer = MerchantSerializer(merchantInstance)
        
        return SuccessResponse(serializer.data, "Merchant created successfully")
    
class MerchantCouriersView(APIView):
    """
    API view for managing courier drivers associated with a specific merchant.
    Provides endpoints for retrieving courier drivers assigned to a merchant.
    Requires authentication for all operations.
    """
    permission_classes = [IsAuthenticated]

    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Retrieves a paginated list of courier drivers associated with a specific merchant.
        
        Query Parameters:
            merchantId (str): The ID of the merchant to get couriers for
            page (int): The page number to retrieve (default: 1)
            page_size (int): Number of items per page (default: 10)
            
        Returns:
            Response: A paginated list of courier drivers with metadata about the pagination
        """
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('page_size', 10)

        merchantId = kwargs.get('merchantId')

        if not merchantId:
            raise ValueError("Merchant ID is required")
        
        merchant = Merchant.objects.get(id=merchantId)
        courierDrivers = User.objects.filter(role__name="Driver", merchant=merchant).order_by('-createdAt')

        paginator = PageNumberPagination()
        paginator.page_size = pageSize

        paginatedCourierDrivers = paginator.paginate_queryset(courierDrivers, request)

        serializer = CourierSerializer(paginatedCourierDrivers, many=True)

        return SuccessResponse(serializer.data, 
            message = "Courier drivers fetched successfully", 
            meta = {
                "total": paginator.page.paginator.count,
                "page": int(page),
                "pageSize": int(pageSize),
                "totalPages": paginator.page.paginator.num_pages,
                "hasNext": paginator.page.has_next(),
                "hasPrevious": paginator.page.has_previous()
        })
    
    