from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contact
from ..serializers import ContactSerializer
from ..utils.ExceptionUtils import ApiExceptionHandler

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContactListView(generics.ListCreateAPIView):
    """
    View for listing all contacts and creating new contacts.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @ApiExceptionHandler
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class ContactDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a single contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]