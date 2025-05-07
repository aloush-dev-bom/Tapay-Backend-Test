from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *

User = get_user_model()

class OrderSerializer(serializers.ModelSerializer):
    merchantName = serializers.SerializerMethodField()
    merchantId = serializers.SerializerMethodField()
    statusName = serializers.SerializerMethodField()
    statusId = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "title",
            "amount",
            "customerName",
            "addressText",
            "addressLongitude",
            "addressLatitude",
            "additionalNotes",
            "createdAt",
            "merchantName",
            "merchantId",
            "statusName",
            "statusId"
        ]

    def get_merchantName(self, obj):
        return obj.merchant.name
    
    def get_merchantId(self, obj):
        return obj.merchant.id
    
    def get_statusName(self, obj):
        return obj.status.name
    
    def get_statusId(self, obj):
        return obj.status.id
    
class OrderAssignmentSerializer(serializers.ModelSerializer):
    userFullName = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()

    class Meta:
        model = OrderAssignment
        fields = ['id', 'user', 'isActive', 'userFullName', 'userEmail', 'assignedAt']

    def get_userFullName(self, obj):
        return obj.user.fullName
    
    def get_userEmail(self, obj):
        return obj.user.email

class SingleOrderSerializer(serializers.ModelSerializer):
    merchantName = serializers.SerializerMethodField()
    merchantId = serializers.SerializerMethodField()
    statusName = serializers.SerializerMethodField()
    statusId = serializers.SerializerMethodField()
    orderAssignments = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "title",
            "amount",
            "customerName",
            "addressText",
            "addressLongitude",
            "addressLatitude",
            "additionalNotes",
            "createdAt",
            "merchantName",
            "merchantId",
            "statusName",
            "statusId",
            "orderAssignments"
        ]

    def get_merchantName(self, obj):
        return obj.merchant.name
    
    def get_merchantId(self, obj):
        return obj.merchant.id
    
    def get_statusName(self, obj):
        return obj.status.name
    
    def get_statusId(self, obj):
        return obj.status.id
    
    def get_orderAssignments(self, obj):
        return OrderAssignmentSerializer(OrderAssignment.objects.filter(order=obj), many=True).data

class TransactionSerializer(serializers.ModelSerializer):
    merchantName = serializers.SerializerMethodField()
    merchantId = serializers.SerializerMethodField()
    statusName = serializers.SerializerMethodField()
    statusId = serializers.SerializerMethodField()
    orderId = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "paymentMethod",
            "balanceAfter",
            "cardNumber",
            "createdAt",
            "merchantName",
            "merchantId",
            "statusName",
            "statusId",
            "orderId"
        ]
    
    def get_merchantName(self, obj):
        return obj.merchant.name
    
    def get_merchantId(self, obj):
        return obj.merchant.id
    
    def get_statusName(self, obj):
        return obj.transactionStatus.name
    
    def get_statusId(self, obj):
        return obj.transactionStatus.id
    
    def get_orderId(self, obj):
        return obj.order.id

class UserSerializer(serializers.ModelSerializer):
    roleName = serializers.SerializerMethodField()
    merchantName = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'fullName', 'is_active', 'is_staff', 'emailVerified', 'phoneNumber', 'role', 'roleName', 'merchant', 'merchantName')
        read_only_fields = ('id', 'email', 'is_active', 'is_staff', 'role', 'roleName', 'merchant', 'merchantName')
    
    def get_roleName(self, obj):
        if obj.role:
            return obj.role.name
        else:
            return None
    
    def get_merchantName(self, obj):
        if obj.merchant:
            return obj.merchant.name
        else:
            return None

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['fullName'] = user.fullName
        token['is_staff'] = user.is_staff
        
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'fullName', 'password', 'password2', 'phoneNumber')
        extra_kwargs = {
            'email': {'required': True},
            'fullName': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'businessName', 'contactName', 'email', 'phone', 
                 'businessType', 'driversCount', 'message', 'createdAt']
        read_only_fields = ['id', 'createdAt']

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'contactEmail', 'contactPhone', 'address', 'isActive', 'currentBalance']
        read_only_fields = ['id', 'createdAt']

class CourierSerializer(serializers.ModelSerializer):
    totalOrders = serializers.SerializerMethodField()
    ordersByStatus = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullName', 'is_active', 'phoneNumber', 'totalOrders', 'ordersByStatus']
        read_only_fields = ['id']

    def get_totalOrders(self, obj):
        return OrderAssignment.objects.filter(user=obj, isActive=True).count()

    def get_ordersByStatus(self, obj):
        assignments = OrderAssignment.objects.filter(user=obj, isActive=True)
        orders = Order.objects.filter(id__in=assignments.values_list('order', flat=True))
        
        statusCounts = {}
        for order in orders:
            status = order.status.name
            statusCounts[status] = statusCounts.get(status, 0) + 1
            
        return statusCounts

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'type']
        read_only_fields = ['id']