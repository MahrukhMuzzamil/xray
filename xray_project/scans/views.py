from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import XRayScan
from .serializers import XRayScanSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q as DjangoQ, Case, When
import logging
import traceback

logger = logging.getLogger(__name__)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class XRayScanViewSet(viewsets.ModelViewSet):
    queryset = XRayScan.objects.all().order_by('-scan_date')
    serializer_class = XRayScanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['body_part', 'institution', 'diagnosis']
    search_fields = ['description', 'diagnosis', 'tags']

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f" Upload request received")
            logger.info(f"   Files: {list(request.FILES.keys()) if request.FILES else 'No files'}")
            logger.info(f"   Data keys: {list(request.data.keys()) if request.data else 'No data'}")
            
            # Check if image file is present
            if 'image' not in request.FILES:
                logger.error(" No image file in request")
                return Response(
                    {'image': ['Image file is required.']}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Log file details
            image_file = request.FILES['image']
            logger.info(f"   Image file: {image_file.name}, size: {image_file.size}, type: {image_file.content_type}")
            
            # Create serializer with request data
            serializer = self.get_serializer(data=request.data)
            
            if not serializer.is_valid():
                logger.error(f"❌ Upload validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            logger.info("✅ Validation passed, saving instance...")
            
            # Save the instance
            instance = serializer.save()
            logger.info(f"✅ Upload successful for scan ID: {instance.id}")
            logger.info(f"   Image URL: {instance.image}")
            
            response_data = serializer.data
            logger.info(f"✅ Returning response: {response_data}")
            
            return Response(response_data, status=status.HTTP_201_CREATED)            
            
        except Exception as e:
            logger.error(f"❌ Upload failed with exception: {str(e)}")
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return Response(
                {'error': f'Upload failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        base_queryset = super().get_queryset()
        search_query = self.request.query_params.get('search')

        if not search_query:
            return base_queryset

        try:
            from .documents import XRayScanDocument
            from elasticsearch_dsl import Q

            q = Q('multi_match', query=search_query, fields=[
                'description', 'diagnosis', 'tags', 'body_part', 'institution', 'patient_id'
            ], fuzziness='auto')

            search = XRayScanDocument.search().query(q)
            results = search.execute()
            ids = [int(hit.meta.id) for hit in results if hit.meta.id.isdigit()]

            if ids:
                preserved_order = Case(
                    *[When(id=id, then=pos) for pos, id in enumerate(ids)]
                )
                return base_queryset.filter(id__in=ids).order_by(preserved_order)

        except Exception as e:
            logger.warning(f"⚠️ Elasticsearch search failed: {e}")

        # fallback to DB query
        return base_queryset.filter(
            DjangoQ(description__icontains=search_query) |
            DjangoQ(diagnosis__icontains=search_query) |
            DjangoQ(tags__icontains=search_query) |
            DjangoQ(body_part__icontains=search_query) |
            DjangoQ(institution__icontains=search_query) |
            DjangoQ(patient_id__icontains=search_query)
        )