from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import XRayScanViewSet

router = DefaultRouter()
router.register(r'scans', XRayScanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
