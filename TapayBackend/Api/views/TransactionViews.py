"""
Transaction views for the API application.
This module contains views for transaction-related operations.
"""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from ..models import Transaction, Merchant, Order, Status, TransactionHistory
from ..serializers import TransactionSerializer
from ..utils.ResponseUtils import SuccessResponse, ErrorResponse
from ..utils.ExceptionUtils import ApiExceptionHandler
from ..utils.TransactionUtils import UpdateTransactionFields


class TransactionsView(APIView):
    """
    API view for handling operations on multiple transactions.
    """

    permission_classes = [permissions.IsAuthenticated]
    
    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Get all transactions for a specific order.
        
        Args:
            request: The HTTP request
            merchantId: The ID of the merchant (from URL)
            orderId: The ID of the order (from URL)
            
        Returns:
            Response: List of transactions
        """
        merchant_id = kwargs.get('merchantId')
        order_id = kwargs.get('orderId')

        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('page_size', 10)
        
        # Get all transactions for a specific order
        transactions = Transaction.objects.filter(merchant=merchant_id, order=order_id).order_by('-createdAt')

        paginator = PageNumberPagination()
        paginator.page_size = pageSize

        paginatedTransactions = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(paginatedTransactions, many=True)
        
        return SuccessResponse({
            "transactions": serializer.data
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
        Create a new transaction for an order.
        
        Args:
            request: The HTTP request
            merchantId: The ID of the merchant (from URL)
            orderId: The ID of the order (from URL)
            
        Returns:
            Response: The created transaction ID
        """
        data = request.data
        merchant_id = kwargs.get('merchantId')
        order_id = kwargs.get('orderId')

        amount = data.get("amount")
        payment_method = data.get("paymentMethod")
        card_number = data.get("cardNumber") 
        transaction_status = data.get("status")

        if payment_method == "Card" and (card_number == "" or card_number is None):
            return ErrorResponse("Card number is required")

        merchant_instance = Merchant.objects.get(pk=merchant_id)
        order_instance = Order.objects.get(pk=order_id)

        transaction_instance = Transaction.objects.create(
            amount=amount,
            paymentMethod=payment_method,
            cardNumber=card_number,
            balanceAfter=merchant_instance.currentBalance + amount,
            transactionStatus=Status.objects.get(name=transaction_status, type="Transaction"),
            merchant=merchant_instance,
            order=order_instance
        )

        return SuccessResponse(
            {"transactionId": transaction_instance.pk},
            message="Transaction created successfully",
            status_code=status.HTTP_201_CREATED
        )

class SingleTransactionView(APIView):
    """
    API view for handling operations on a single transaction.
    """

    permission_classes = [permissions.IsAuthenticated]
    
    @ApiExceptionHandler
    def get(self, request, *args, **kwargs):
        """
        Get a single transaction with its history.
        
        Args:
            request: The HTTP request
            merchantId: The ID of the merchant (from URL)
            orderId: The ID of the order (from URL)
            transactionId: The ID of the transaction (from URL)
            
        Returns:
            Response: The transaction and its history
        """
        merchant_id = kwargs.get('merchantId')
        order_id = kwargs.get('orderId')
        transaction_id = kwargs.get('transactionId')
        
        transaction = Transaction.objects.get(
            pk=transaction_id,
            merchant__id=merchant_id,
            order__id=order_id
        )
        
        serializer = TransactionSerializer(transaction)
        
        # Get transaction history
        history = TransactionHistory.objects.filter(transaction=transaction).order_by('-createdAt')
        history_data = []
        
        for item in history:
            history_data.append({
                "fieldChanged": item.fieldChanged,
                "oldValue": item.oldValue,
                "newValue": item.newValue,
                "createdAt": item.createdAt
            })
        
        return SuccessResponse({
            "transaction": serializer.data,
            "history": history_data
        })
    
    @ApiExceptionHandler
    def put(self, request, *args, **kwargs):
        """
        Update a single transaction.
        
        Args:
            request: The HTTP request
            merchantId: The ID of the merchant (from URL)
            orderId: The ID of the order (from URL)
            transactionId: The ID of the transaction (from URL)
            
        Returns:
            Response: The updated transaction
        """
        data = request.data
        merchant_id = kwargs.get('merchantId')
        order_id = kwargs.get('orderId')
        transaction_id = kwargs.get('transactionId')
        
        # Get the transaction instance
        transaction_instance = Transaction.objects.get(
            pk=transaction_id, 
            merchant__id=merchant_id, 
            order__id=order_id
        )
        
        # Update transaction fields and track changes
        transaction_instance, changes = UpdateTransactionFields(transaction_instance, data)
        
        # Return the updated transaction
        if changes:
            serializer = TransactionSerializer(transaction_instance)
            return SuccessResponse(
                {"transaction": serializer.data},
                message="Transaction updated successfully"
            )
        else:
            return SuccessResponse(
                {},
                message="No changes detected"
            ) 