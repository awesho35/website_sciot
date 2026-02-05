"""
URL configuration for Sciot API project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Django admin (backup)
    path('django-admin/', admin.site.urls),
    
    # Custom admin panel
    path('admin-panel/', include('admin_custom.urls')),
    
    # API endpoints
    path('api/', include('core.urls')),
    path('api/events/', include('events.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/media/', include('media_manager.urls')),
    path('api/pages/', include('pages.urls')),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
