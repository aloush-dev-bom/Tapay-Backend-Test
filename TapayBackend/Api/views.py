"""
Views for the API application.
This module imports views from the views package for backward compatibility.
"""

# Import views from the views package
from .views.OrderViews import MerchantOrdersView, SingleOrderView, CourierOrdersView
from .views.TransactionViews import TransactionsView, SingleTransactionView
from .views.AuthViews import (
    CustomTokenObtainPairView, RegisterView, ChangePasswordView,
    UserProfileView, LogoutView
)
from .views.OrderAssignmentView import OrderAssignmentView
from .views.ContactViews import ContactListView, ContactDetailView

# For backward compatibility
__all__ = [
    'MerchantOrdersView',
    'SingleOrderView',

    'CourierOrdersView',

    'OrderAssignmentView',

    'TransactionsView',
    'SingleTransactionView',
    
    'CustomTokenObtainPairView',
    'RegisterView',
    'ChangePasswordView',
    'UserProfileView',
    'LogoutView',

    'ContactListView',
    'ContactDetailView',
] 