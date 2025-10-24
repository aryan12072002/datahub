from rest_framework import serializers
from .models import DataSource, Record

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'endpoint_url', 'active']

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'source', 'key', 'value', 'last_updated']
