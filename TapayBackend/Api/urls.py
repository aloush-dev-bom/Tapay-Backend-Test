from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, RegisterView, ChangePasswordView, UserProfileView, LogoutView,
    MerchantOrdersView, SingleOrderView, TransactionsView, SingleTransactionView, CourierOrdersView,
    MerchantsView, MerchantCouriersView, StatusListView
)
from .views.OrderAssignmentView import OrderAssignmentView
from .views.ContactViews import ContactListView, ContactDetailView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path("merchants/", MerchantsView.as_view(), name='merchants'),
    
    path("merchants/<int:merchantId>/couriers/", MerchantCouriersView.as_view(), name='merchant-couriers'),

    path("merchants/<int:merchantId>/orders/", MerchantOrdersView.as_view(), name='merchant-orders'),
    path("merchants/<int:merchantId>/orders/<int:orderId>/", SingleOrderView.as_view(), name='single-order'),
    path("merchants/<int:merchantId>/orders/<int:orderId>/transactions/", TransactionsView.as_view(), name='transactions'),
    path("merchants/<int:merchantId>/orders/<int:orderId>/transactions/<int:transactionId>/", SingleTransactionView.as_view(), name='single-transaction'),
    path("merchants/<int:merchantId>/orders/<int:orderId>/order-assignments/", OrderAssignmentView.as_view(), name='order-assignments'),

    path("couriers/<str:courierId>/orders/", CourierOrdersView.as_view(), name='courier-orders'),
    
    path("contacts/", ContactListView.as_view(), name='contact-list'),
    path("contacts/<int:pk>/", ContactDetailView.as_view(), name='contact-detail'),

    path("statuses/", StatusListView.as_view(), name='status-list'),
]