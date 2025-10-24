from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSourceViewSet, stats_view

router = DefaultRouter()
router.register(r'sources', DataSourceViewSet, basename='sources')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', stats_view),
]
