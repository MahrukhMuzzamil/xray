from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scans.urls')),
]

# 👇 Serve media always (development and Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
