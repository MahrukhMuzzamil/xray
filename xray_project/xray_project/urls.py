from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scans.urls')),  # this pulls in the app's routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
