from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import XRayScan
from .serializers import XRayScanSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q as DjangoQ, Case, When


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
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

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
            print(f"⚠️ Elasticsearch search failed: {e}")

        # fallback to DB query
        return base_queryset.filter(
            DjangoQ(description__icontains=search_query) |
            DjangoQ(diagnosis__icontains=search_query) |
            DjangoQ(tags__icontains=search_query) |
            DjangoQ(body_part__icontains=search_query) |
            DjangoQ(institution__icontains=search_query) |
            DjangoQ(patient_id__icontains=search_query)
        )
