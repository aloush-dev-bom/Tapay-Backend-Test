from rest_framework import generics
from Api.models import Status
from Api.serializers import StatusSerializer
from Api.utils.ExceptionUtils import ApiExceptionHandler

class StatusListView(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    pagination_class = None

    @ApiExceptionHandler
    def get_queryset(self):
        queryset = Status.objects.all()
        type_param = self.request.query_params.get('type', None)
        if type_param:
            queryset = queryset.filter(type=type_param)
        return queryset