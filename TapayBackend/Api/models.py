from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullName, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullName=fullName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullName, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, fullName, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    fullName = models.CharField(max_length=255)
    
    # Status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Role and Merchant
    role = models.ForeignKey(to = "Role", on_delete = models.RESTRICT, null=True, blank=True)
    merchant = models.ForeignKey(to = "Merchant", on_delete = models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)
    lastLogin = models.DateTimeField(null=True, blank=True)
    
    # Additional fields for security
    emailVerified = models.BooleanField(default=False)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    
    # Login attempts tracking for security
    failedLoginAttempts = models.PositiveIntegerField(default=0)
    lastFailedLogin = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-createdAt']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.fullName

    def get_short_name(self):
        return self.fullName.split()[0]
    
    def clean(self):
        super().clean()
        if self.role.requiresMerchant and not self.merchant:
            raise ValidationError(f"Users with role '{self.role.name}' must be associated with a merchant")

class Role(models.Model):
    name = models.CharField(max_length = 255)
    requiresMerchant = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Merchant(models.Model):
    name = models.CharField(max_length = 255)
    contactEmail = models.CharField(max_length = 255)
    contactPhone = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    isActive = models.BooleanField(default = 1)
    currentBalance = models.FloatField(default = 0)

    createdAt = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    title = models.CharField(max_length = 255)
    amount = models.FloatField()
    customerName = models.CharField(max_length = 255)
    addressText = models.CharField(max_length = 255)
    addressLongitude = models.FloatField(blank = True, null = True)
    addressLatitude = models.FloatField(blank = True, null = True)
    additionalNotes = models.TextField(blank = True, null = True)

    createdAt = models.DateTimeField(auto_now_add = True)

    status = models.ForeignKey(to = "Status", on_delete = models.RESTRICT)
    merchant = models.ForeignKey(to = "Merchant", on_delete = models.RESTRICT)
    orderAssignments = models.ManyToManyField(to = "User", through = "OrderAssignment")

class OrderAssignment(models.Model):
    order = models.ForeignKey(to = "Order", on_delete = models.RESTRICT)
    user = models.ForeignKey(to = "User", on_delete = models.RESTRICT)

    assignedAt = models.DateTimeField(auto_now_add = True)
    isActive = models.BooleanField(default = True)
    
    def __str__(self):
        return f"{self.user.fullName} - {self.order.title}"

class Transaction(models.Model):
    amount = models.FloatField()
    paymentMethod = models.CharField(max_length = 255)
    balanceAfter = models.FloatField()
    cardNumber = models.CharField(max_length = 255, blank = True, null = True)

    createdAt = models.DateTimeField(auto_now_add = True)

    transactionStatus = models.ForeignKey(to = "Status", on_delete = models.RESTRICT)
    merchant = models.ForeignKey(to = "Merchant", on_delete = models.RESTRICT)
    order = models.ForeignKey(to = "Order", on_delete = models.RESTRICT)

class TransactionHistory(models.Model):
    fieldChanged = models.CharField(max_length = 255)
    oldValue = models.CharField(max_length = 255)
    newValue = models.CharField(max_length = 255)

    createdAt = models.DateTimeField(auto_now_add = True)

    transaction = models.ForeignKey(to = "Transaction", on_delete = models.RESTRICT)

    def __str__(self):
        return f"{self.fieldChanged}: {self.oldValue} -> {self.newValue}"

class Status(models.Model):
    name = models.CharField(max_length = 255)
    type = models.CharField(max_length = 255)

    def __str__(self):
        return f"{self.type} | {self.name}"
    
class Contact(models.Model):
    businessName = models.CharField(max_length = 255)
    contactName = models.CharField(max_length = 255)
    email = models.EmailField()
    phone = models.CharField(max_length = 255)
    businessType = models.CharField(max_length = 255)
    driversCount = models.CharField(max_length = 255)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.businessName} - {self.contactName}"
    
    class Meta:
        ordering = ['createdAt']