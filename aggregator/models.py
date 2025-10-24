from django.db import models

class DataSource(models.Model):
    name = models.CharField(max_length=200)
    endpoint_url = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)

class Record(models.Model):
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='records')
    key = models.CharField(max_length=255)
    value = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('source', 'key')
