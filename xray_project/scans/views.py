from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import XRayScan
from .serializers import XRayScanSerializer
from django_filters.rest_framework import DjangoFilterBackend

class XRayScanViewSet(viewsets.ModelViewSet):
    queryset = XRayScan.objects.all().order_by('-scan_date')
    serializer_class = XRayScanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['body_part', 'institution', 'diagnosis']
    search_fields = ['description', 'diagnosis', 'tags']

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Upload failed with errors:")
            print(serializer.errors)  # 🔍 DEBUG: Shows you what caused 400 error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)

        if not search_query:
            return super().get_queryset()

        try:
            from .documents import XRayScanDocument
            from elasticsearch_dsl import Q

            q = Q(
                'multi_match',
                query=search_query,
                fields=['description', 'diagnosis', 'tags', 'body_part', 'institution', 'patient_id'],
                type='best_fields'
            )

            search = XRayScanDocument.search().query(q)
            response = search.execute()
            ids = [hit.meta.id for hit in response]

            if ids:
                preserved_order = 'CASE scans_xrayscan.id '
                for i, id in enumerate(ids):
                    preserved_order += f'WHEN {id} THEN {i} '
                preserved_order += 'END'

                queryset = XRayScan.objects.filter(id__in=ids).extra(
                    select={'ordering': preserved_order},
                    order_by=('ordering',)
                )
                return queryset

        except Exception as e:
            print(f"Elasticsearch search failed: {e}")

        return super().get_queryset().filter(
            description__icontains=search_query
        ) | super().get_queryset().filter(
            diagnosis__icontains=search_query
        ) | super().get_queryset().filter(
            tags__icontains=search_query
        )
