import random, time
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from .models import DataSource, Record

@shared_task
def fetch_and_upsert_for_source(source_id):
    ds = DataSource.objects.get(pk=source_id)
    n = random.randint(10, 50)
    now = timezone.now()
    items = [(f"k_{i}", {"val": random.random()}) for i in range(n)]
    existing = Record.objects.filter(source=ds, key__in=[k for k, _ in items]).in_bulk(field_name='key')
    to_create, to_update = [], []

    for key, value in items:
        rec = existing.get(key)
        if rec:
            rec.value = value
            rec.last_updated = now
            to_update.append(rec)
        else:
            to_create.append(Record(source=ds, key=key, value=value))

    with transaction.atomic():
        if to_create:
            Record.objects.bulk_create(to_create)
        if to_update:
            Record.objects.bulk_update(to_update, ['value', 'last_updated'])
    cache.delete('api:stats')

@shared_task
def aggregate_all_sources():
    for ds in DataSource.objects.filter(active=True):
        fetch_and_upsert_for_source(ds.id)
