"""
URL configuration for Sciot API project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
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

# Serve media files — always active so the platform nginx can proxy /media/ to this container.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
