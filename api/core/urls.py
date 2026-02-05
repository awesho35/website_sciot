from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'social-links', views.SocialLinkViewSet)
router.register(r'contact', views.ContactMessageViewSet)

urlpatterns = [
    path('config/', views.site_config, name='site-config'),
    path('config/update/', views.update_site_config, name='site-config-update'),
    path('', include(router.urls)),
]
