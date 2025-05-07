from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Merchant, Order, Transaction, Status, OrderAssignment, Role, Contact

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'fullName', 'role', 'is_active', 'is_staff', 'emailVerified', 'createdAt', 'lastLogin')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'emailVerified', 'createdAt', 'role')
    search_fields = ('email', 'fullName', 'phoneNumber')
    ordering = ('-createdAt',)
    
    # Fields to show when creating/editing a user
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal info'), {
            'fields': ('fullName', 'phoneNumber')
        }),
        (_('Status'), {
            'fields': ('emailVerified', 'is_active', 'is_staff', 'is_superuser')
        }),
        (_('Access'), {
            'fields': ('role', 'merchant')
        }),
        (_('Security'), {
            'fields': ('failedLoginAttempts', 'lastFailedLogin')
        }),
        (_('Important dates'), {
            'fields': ('lastLogin', 'createdAt', 'updatedAt')
        }),
        (_('Permissions'), {
            'fields': ('groups', 'user_permissions'),
        }),
    )

    # Fields shown when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullName', 'password1', 'password2', 'role', 'merchant'),
        }),
    )

    readonly_fields = ('createdAt', 'updatedAt', 'lastLogin', 'failedLoginAttempts', 'lastFailedLogin')
    
    # Custom actions
    actions = ['activate_users', 'deactivate_users', 'reset_failed_login_attempts']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

    def reset_failed_login_attempts(self, request, queryset):
        queryset.update(failedLoginAttempts=0, lastFailedLogin=None)
    reset_failed_login_attempts.short_description = "Reset failed login attempts"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('businessName', 'contactName', 'email', 'phone', 'businessType', 'driversCount', 'createdAt')
    list_filter = ('businessType', 'createdAt')
    search_fields = ('businessName', 'contactName', 'email', 'phone')
    readonly_fields = ('createdAt',)
    ordering = ('-createdAt',)
    
    fieldsets = (
        (_('Business Information'), {
            'fields': ('businessName', 'businessType', 'driversCount')
        }),
        (_('Contact Information'), {
            'fields': ('contactName', 'email', 'phone')
        }),
        (_('Message'), {
            'fields': ('message',)
        }),
        (_('Timestamps'), {
            'fields': ('createdAt',)
        }),
    )

# Register other models
admin.site.register(Merchant)
admin.site.register(Order)
admin.site.register(OrderAssignment)
admin.site.register(Transaction)
admin.site.register(Status)
admin.site.register(Role)