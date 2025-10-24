from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.core.cache import cache
from .models import DataSource, Record
from .serializers import DataSourceSerializer
from .tasks import fetch_and_upsert_for_source
from django.conf import settings

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

    @action(detail=True, methods=['post'])
    def fetch(self, request, pk=None):
        ds = self.get_object()
        task = fetch_and_upsert_for_source.delay(ds.id)
        return Response({'task_id': task.id, 'status': 'started'})

@api_view(['GET'])
def stats_view(request):
    cache_key = 'api:stats'
    cached = cache.get(cache_key)
    if cached:
        return Response({'cached': True, **cached})

    total_sources = DataSource.objects.count()
    total_records = Record.objects.count()
    data = {'total_sources': total_sources, 'total_records': total_records}
    cache.set(cache_key, data, timeout=settings.CACHE_TTL)
    return Response({'cached': False, **data})
