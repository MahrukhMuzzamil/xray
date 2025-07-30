from rest_framework import viewsets, filters
from .models import XRayScan
from .serializers import XRayScanSerializer
from django_filters.rest_framework import DjangoFilterBackend

class XRayScanViewSet(viewsets.ModelViewSet):
    queryset = XRayScan.objects.all().order_by('-scan_date')
    serializer_class = XRayScanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['body_part', 'institution', 'diagnosis']
    search_fields = ['description', 'diagnosis', 'tags']
